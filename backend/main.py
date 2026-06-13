from fastapi import FastAPI, Depends, HTTPException, status, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import asyncio

from backend.config import get_settings
from backend.database import get_db, init_db, close_db
from backend.models import User, UserProfile, Message, Plan, Event, Exam, Memory, AdminRequest, Complaint
from backend.schemas import (
    UserRegister, UserLogin, UserResponse, TokenResponse,
    UserProfileUpdate, UserProfileResponse, ChatRequest, ChatResponse,
    PlanCreate, PlanUpdate, PlanResponse,
    EventCreate, EventResponse,
    ExamResponse,
)
from typing import List
import json as _json
from backend.auth import (
    hash_password, verify_password, verify_token,
    create_access_token, create_refresh_token, TokenData
)
from backend.agents import orchestrator
from backend.services.memory_manager import get_memory_manager

settings = get_settings()

# Create FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for SmartStudent - AI-powered student assistant"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Startup and shutdown events
@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    init_db()
    _seed_demo_data()

def _seed_demo_data():
    """Insère des événements et tâches de démo si la base est vide."""
    db = next(get_db())
    try:
        if db.query(Event).count() == 0:
            now = datetime.utcnow()
            demo_events = [
                Event(title="Conférence IA & LLMs", description="Présentation des dernières avancées en intelligence artificielle et grands modèles de langage.", event_type="conference", start_date=now + timedelta(days=3), location="Amphithéâtre A", is_public=True),
                Event(title="Journée Portes Ouvertes", description="Découvrez les filières et projets de fin d'études.", event_type="event", start_date=now + timedelta(days=7), location="Hall principal", is_public=True),
                Event(title="Workshop Flutter", description="Atelier pratique : créer une application mobile Flutter de A à Z.", event_type="workshop", start_date=now + timedelta(days=10), location="Salle TP3", is_public=True),
                Event(title="Deadline projet PFA", description="Remise du rapport d'avancement.", event_type="deadline", start_date=now + timedelta(days=14), location=None, is_public=True),
                Event(title="Forum Entreprises", description="Rencontrez 50+ recruteurs pour stages et emplois.", event_type="event", start_date=now + timedelta(days=21), location="Centre de conférences", is_public=True),
            ]
            db.add_all(demo_events)
            db.commit()
    except Exception:
        db.rollback()
    finally:
        db.close()

@app.on_event("shutdown")
async def shutdown_event():
    """Close database connections on shutdown"""
    close_db()

# ==================== HEALTH CHECK ====================

@app.get("/health", tags=["Health"])
async def health_check():
    """Health check endpoint"""
    return {
        "status": "ok",
        "service": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": datetime.utcnow().isoformat()
    }

# ==================== AUTHENTICATION ROUTES ====================

@app.post("/api/auth/register", response_model=TokenResponse, tags=["Auth"])
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    """Register a new user"""
    
    # Check if user already exists
    existing_user = db.query(User).filter(
        (User.email == user_data.email) | (User.username == user_data.username)
    ).first()
    
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email or username already registered"
        )
    
    # Derive first/last from full_name if not provided separately
    first_name = user_data.first_name or (user_data.full_name.split()[0] if user_data.full_name else None)
    last_name  = user_data.last_name  or (" ".join(user_data.full_name.split()[1:]) if user_data.full_name and len(user_data.full_name.split()) > 1 else None)

    # Create new user
    db_user = User(
        email=user_data.email,
        username=user_data.username,
        full_name=user_data.full_name,
        first_name=first_name,
        last_name=last_name,
        hashed_password=hash_password(user_data.password)
    )
    db.add(db_user)
    db.flush()

    # Create user profile with academic data
    db_profile = UserProfile(
        user_id=db_user.id,
        student_card_id=user_data.student_card_id,
        major=user_data.field_of_study,
        year=user_data.academic_year,
    )
    db.add(db_profile)
    db.commit()
    db.refresh(db_user)

    # Generate tokens enriched with student context
    _token_kwargs = dict(
        user_id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        first_name=first_name,
        last_name=last_name,
        student_card_id=user_data.student_card_id,
        field_of_study=user_data.field_of_study,
        academic_year=user_data.academic_year,
    )
    access_token = create_access_token(**_token_kwargs)
    refresh_token = create_refresh_token(**_token_kwargs)
    
    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(db_user)
    )

@app.post("/api/auth/login", response_model=TokenResponse, tags=["Auth"])
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Login user and return tokens"""
    
    # Find user by email
    db_user = db.query(User).filter(User.email == credentials.email).first()
    
    if not db_user or not verify_password(credentials.password, db_user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )
    
    if not db_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is disabled"
        )
    
    # Fetch profile to enrich JWT with student context
    _profile = db.query(UserProfile).filter(UserProfile.user_id == db_user.id).first()
    _token_kwargs = dict(
        user_id=db_user.id,
        username=db_user.username,
        email=db_user.email,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        student_card_id=getattr(_profile, "student_card_id", None),
        field_of_study=getattr(_profile, "major", None),
        academic_year=getattr(_profile, "year", None),
    )
    access_token = create_access_token(**_token_kwargs)
    refresh_token = create_refresh_token(**_token_kwargs)

    return TokenResponse(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
        user=UserResponse.model_validate(db_user)
    )

from pydantic import BaseModel as _PydanticBaseModel

class RefreshRequest(_PydanticBaseModel):
    refresh_token: str

@app.post("/api/auth/refresh", tags=["Auth"])
async def refresh_token(body: RefreshRequest, db: Session = Depends(get_db)):
    """Exchange a valid refresh token for a new access token"""
    from jose import JWTError, jwt as _jwt
    try:
        payload = _jwt.decode(body.refresh_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        user_id = payload.get("user_id")
        user = db.query(User).filter(User.id == user_id).first()
        if not user or not user.is_active:
            raise HTTPException(status_code=401, detail="User not found or inactive")
        _profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        new_access = create_access_token(
            user_id=user.id,
            username=user.username,
            email=user.email,
            first_name=user.first_name,
            last_name=user.last_name,
            student_card_id=getattr(_profile, "student_card_id", None),
            field_of_study=getattr(_profile, "major", None),
            academic_year=getattr(_profile, "year", None),
        )
        return {
            "access_token": new_access,
            "token_type": "bearer",
            "expires_in": settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60
        }
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

# Helper function to get current user
async def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """Get current authenticated user from token"""
    
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing or invalid authorization header"
        )
    
    token = authorization.replace("Bearer ", "")
    token_data = verify_token(token)
    
    if not token_data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token"
        )
    
    user = db.query(User).filter(User.id == token_data.user_id).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    return user

# ==================== USER PROFILE ROUTES ====================

@app.get("/api/user/profile", response_model=UserProfileResponse, tags=["User"])
async def get_profile(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Get current user's profile"""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    return UserProfileResponse.model_validate(profile)

@app.put("/api/user/profile", response_model=UserProfileResponse, tags=["User"])
async def update_profile(
    profile_data: UserProfileUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Update user profile"""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Profile not found"
        )
    
    # Update fields
    for key, value in profile_data.dict(exclude_unset=True).items():
        setattr(profile, key, value)
    
    profile.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(profile)
    
    return UserProfileResponse.model_validate(profile)

# ==================== MEMORY HELPER ====================

def _save_memory_if_relevant(db: Session, user_id: int, user_message: str, agent_resp: dict):
    """Extract and persist key facts from the conversation to long-term memory."""
    agent = agent_resp.get("agent", "")
    response_text = agent_resp.get("response", "")

    # Patterns that indicate memorable information
    memory_triggers = {
        "preferences": ["je préfère", "j'aime", "je n'aime pas", "je veux", "mon objectif"],
        "academic": ["ma filière", "mon semestre", "mon projet", "mon pfe", "mon stage",
                     "je suis en", "j'étudie", "ma spécialité"],
        "personal": ["je m'appelle", "j'habite", "mon email", "mon numéro"],
    }

    msg_lower = user_message.lower()
    for category, triggers in memory_triggers.items():
        if any(t in msg_lower for t in triggers):
            # Avoid near-duplicate memories
            existing = db.query(Memory).filter(
                Memory.user_id == user_id,
                Memory.category == category,
            ).order_by(Memory.updated_at.desc()).first()

            content = user_message[:300]
            if existing and existing.content[:100] == content[:100]:
                break

            importance = 3 if category == "academic" else 2
            mem = Memory(
                user_id=user_id,
                category=category,
                content=content,
                importance=importance,
            )
            try:
                db.add(mem)
                db.flush()
            except Exception:
                db.rollback()
            break

    # Always record which agent domains the user frequents (for routing hints)
    if agent and agent != "admin":
        interest_content = f"Intérêt fréquent : module {agent}"
        exists = db.query(Memory).filter(
            Memory.user_id == user_id,
            Memory.category == "preferences",
            Memory.content == interest_content,
        ).first()
        if not exists:
            try:
                db.add(Memory(
                    user_id=user_id,
                    category="preferences",
                    content=interest_content,
                    importance=1,
                ))
                db.flush()
            except Exception:
                db.rollback()


# ==================== CHAT ROUTES ====================

@app.post("/api/chat", response_model=ChatResponse, tags=["Chat"])
async def chat(
    request: ChatRequest,
    background_tasks: BackgroundTasks,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Send message to orchestrator agent"""
    
    user = await get_current_user(authorization, db)
    
    # Get user profile for context
    user_profile = db.query(UserProfile).filter(
        UserProfile.user_id == user.id
    ).first()
    
    # Get conversation history (last 10 messages)
    conversation_history = []
    recent_messages = db.query(Message).filter(
        Message.user_id == user.id
    ).order_by(Message.created_at.desc()).limit(10).all()
    
    for msg in reversed(recent_messages):
        conversation_history.append({
            "role": msg.sender,
            "content": msg.content
        })
    
    # Load long-term memories for this user
    user_memories = db.query(Memory).filter(
        Memory.user_id == user.id,
        (Memory.expires_at == None) | (Memory.expires_at > datetime.utcnow())
    ).order_by(Memory.importance.desc(), Memory.updated_at.desc()).limit(10).all()

    # Build rich user context
    user_context = {
        "user_id": user.id,
        "conversation_id": request.conversation_id or f"user_{user.id}",
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email,
        "university": user_profile.university if user_profile else None,
        "major": user_profile.major if user_profile else None,
        "year": user_profile.year if user_profile else None,
        "language": user_profile.language if user_profile else "en",
        "timezone": user_profile.timezone if user_profile else "UTC",
        "memories": [
            {"category": m.category, "content": m.content, "importance": m.importance}
            for m in user_memories
        ],
    }

    # Process through orchestrator
    orchestrator_response = await orchestrator.process_message(
        user_message=request.message,
        conversation_history=conversation_history,
        user_context=user_context
    )

    # Extract and persist important facts in background (non-blocking)
    background_tasks.add_task(
        get_memory_manager().extract_and_store,
        user.id,
        request.message,
        orchestrator_response["response"],
    )
    
    # Save messages to database
    user_message_db = Message(
        user_id=user.id,
        content=request.message,
        sender="user",
        message_type="text"
    )
    db.add(user_message_db)
    db.flush()
    
    assistant_message_db = Message(
        user_id=user.id,
        content=orchestrator_response["response"],
        sender="assistant",
        message_type="text",
        extra_data={
            "agent": orchestrator_response["agent"],
            "agent_name": orchestrator_response["agent_name"]
        }
    )
    db.add(assistant_message_db)
    db.commit()
    
    return ChatResponse(
        response=orchestrator_response["response"],
        conversation_id=request.conversation_id or str(user.id),
        agent=orchestrator_response["agent"],
        agent_name=orchestrator_response.get("agent_name", ""),
        extra_data=orchestrator_response.get("metadata", {})
    )

# ==================== PLANNING ROUTES ====================

@app.get("/api/planning/tasks", response_model=List[PlanResponse], tags=["Planning"])
async def get_tasks(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    tasks = db.query(Plan).filter(Plan.user_id == user.id).order_by(Plan.due_date).all()
    return tasks

@app.post("/api/planning/tasks", response_model=PlanResponse, tags=["Planning"])
async def create_task(
    task_data: PlanCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    task = Plan(
        user_id=user.id,
        title=task_data.title,
        description=task_data.description,
        category=task_data.category,
        due_date=task_data.due_date,
        priority=task_data.priority,
        status="pending"
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@app.put("/api/planning/tasks/{task_id}", response_model=PlanResponse, tags=["Planning"])
async def update_task(
    task_id: int,
    task_data: PlanUpdate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    task = db.query(Plan).filter(Plan.id == task_id, Plan.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    for key, value in task_data.dict(exclude_unset=True).items():
        setattr(task, key, value)
    task.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(task)
    return task

@app.delete("/api/planning/tasks/{task_id}", tags=["Planning"])
async def delete_task(
    task_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    task = db.query(Plan).filter(Plan.id == task_id, Plan.user_id == user.id).first()
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    db.delete(task)
    db.commit()
    return {"message": "Task deleted"}

# ==================== CAMPUS / EVENTS ROUTES ====================

@app.get("/api/campus/events", response_model=List[EventResponse], tags=["Campus"])
async def get_events(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    await get_current_user(authorization, db)
    events = db.query(Event).filter(Event.is_public == True).order_by(Event.start_date).all()
    return events

@app.post("/api/campus/events", response_model=EventResponse, tags=["Campus"])
async def create_event(
    event_data: EventCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    await get_current_user(authorization, db)
    event = Event(
        title=event_data.title,
        description=event_data.description,
        event_type=event_data.event_type,
        start_date=event_data.start_date,
        end_date=event_data.end_date,
        location=event_data.location,
        is_public=True
    )
    db.add(event)
    db.commit()
    db.refresh(event)
    return event

# ==================== EXAMS ROUTES ====================

@app.get("/api/exams/history", response_model=List[ExamResponse], tags=["Exams"])
async def get_exam_history(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    exams = db.query(Exam).filter(Exam.user_id == user.id).order_by(Exam.created_at.desc()).all()
    return exams

@app.get("/api/exams/stats", tags=["Exams"])
async def get_exam_stats(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    exams = db.query(Exam).filter(Exam.user_id == user.id).all()
    completed = [e for e in exams if e.status == "completed" and e.score is not None]
    avg = sum(e.score / e.total_points * 100 for e in completed) / len(completed) if completed else 0
    return {
        "average_score": round(avg, 1),
        "total_exams": len(exams),
        "completed_exams": len(completed),
        "weak_subjects": [],
        "strong_subjects": []
    }

@app.post("/api/exams/generate", tags=["Exams"])
async def generate_exam(
    request: dict,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    subject = request.get("subject", "Général")
    num_q = int(request.get("num_questions", 5))
    difficulty = request.get("difficulty", "medium")

    # Essai de génération via LLM
    questions = []
    try:
        diff_label = {"easy": "simples", "medium": "de niveau moyen", "hard": "difficiles"}.get(difficulty, "de niveau moyen")
        prompt = (
            f"Génère {num_q} questions QCM {diff_label} sur le sujet : '{subject}'. "
            "Réponds UNIQUEMENT avec un tableau JSON valide, sans texte avant ou après. "
            "Format exact : "
            '[{"question":"...","options":["A. ...","B. ...","C. ...","D. ..."],"answer":"A. ...","explanation":"..."}]'
        )
        llm_result = await orchestrator.process_message(
            user_message=prompt,
            user_context={"user_id": user.id, "generate_quiz": True}
        )
        raw = llm_result.get("response", "")
        start = raw.find("[")
        end = raw.rfind("]") + 1
        if start >= 0 and end > start:
            questions = _json.loads(raw[start:end])
    except Exception:
        pass

    # Fallback : questions génériques si le LLM échoue
    if not questions:
        fallback = {
            "Algorithmique": [
                {"question": "Quelle est la complexité d'un tri à bulles dans le pire cas ?",
                 "options": ["A. O(n)", "B. O(n log n)", "C. O(n²)", "D. O(log n)"],
                 "answer": "C. O(n²)", "explanation": "Le tri à bulles compare chaque paire, d'où O(n²)."},
                {"question": "Quelle structure utilise LIFO ?",
                 "options": ["A. File", "B. Pile", "C. Liste", "D. Arbre"],
                 "answer": "B. Pile", "explanation": "LIFO = Last In First Out, c'est la pile."},
                {"question": "Qu'est-ce qu'un arbre binaire de recherche ?",
                 "options": ["A. Nœuds avec 3 enfants", "B. Gauche < Nœud < Droite", "C. Arbre équilibré", "D. Arbre avec couleurs"],
                 "answer": "B. Gauche < Nœud < Droite", "explanation": "Propriété fondamentale du BST."},
                {"question": "Quel algorithme utilise une file de priorité ?",
                 "options": ["A. BFS", "B. DFS", "C. Dijkstra", "D. Tri rapide"],
                 "answer": "C. Dijkstra", "explanation": "Dijkstra utilise une file de priorité (min-heap)."},
                {"question": "Quel est le meilleur cas du tri rapide ?",
                 "options": ["A. O(n²)", "B. O(n)", "C. O(n log n)", "D. O(1)"],
                 "answer": "C. O(n log n)", "explanation": "Quand le pivot divise équitablement, on obtient O(n log n)."},
            ]
        }
        questions = fallback.get(subject, fallback["Algorithmique"])[:num_q]
        while len(questions) < num_q:
            questions.append(questions[0])
        questions = questions[:num_q]

    exam = Exam(
        user_id=user.id,
        title=f"Quiz {subject} — {difficulty}",
        subject=subject,
        questions=questions,
        total_points=len(questions),
        status="in_progress",
        started_at=datetime.utcnow()
    )
    db.add(exam)
    db.commit()
    db.refresh(exam)

    return {
        "id": exam.id,
        "user_id": exam.user_id,
        "title": exam.title,
        "subject": exam.subject,
        "questions": questions,
        "total_points": exam.total_points,
        "status": exam.status,
        "score": None,
        "created_at": exam.created_at.isoformat(),
        "completed_at": None
    }

@app.post("/api/exams/{exam_id}/submit", tags=["Exams"])
async def submit_exam(
    exam_id: int,
    submission: dict,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    user = await get_current_user(authorization, db)
    exam = db.query(Exam).filter(Exam.id == exam_id, Exam.user_id == user.id).first()
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    answers = submission.get("answers", [])
    questions = exam.questions or []
    score = 0
    feedback = []
    for i, q in enumerate(questions):
        user_ans = answers[i] if i < len(answers) else None
        correct = q.get("answer", "")
        is_correct = user_ans == correct
        if is_correct:
            score += 1
        feedback.append({
            "question": q.get("question", ""),
            "user_answer": user_ans,
            "correct_answer": correct,
            "is_correct": is_correct,
            "explanation": q.get("explanation", "")
        })

    exam.score = score
    exam.answers = answers
    exam.status = "completed"
    exam.completed_at = datetime.utcnow()
    db.commit()

    return {
        "score": score,
        "total": len(questions),
        "percentage": round(score / len(questions) * 100, 1) if questions else 0,
        "feedback": feedback
    }

# ==================== RAG / ADMIN ROUTES ====================

@app.get("/api/admin/rag/status", tags=["Admin RAG"])
async def rag_status():
    """Statut du système RAG."""
    try:
        from backend.services.rag_service import get_rag_service
        rag = get_rag_service()
        return {
            "ready": rag.is_ready,
            "document_count": rag.document_count,
            "message": "RAG opérationnel" if rag.is_ready else "RAG non disponible — lance setup_rag.py"
        }
    except Exception as e:
        return {"ready": False, "document_count": 0, "message": str(e)}

@app.post("/api/admin/rag/search", tags=["Admin RAG"])
async def rag_search(
    request: Request,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Recherche directe dans la base documentaire ENIAD."""
    await get_current_user(authorization, db)
    body = await request.json()
    query = body.get("query", "")
    n = min(int(body.get("n_results", 5)), 10)
    if not query:
        raise HTTPException(status_code=400, detail="query required")
    try:
        from backend.services.rag_service import get_rag_service
        rag = get_rag_service()
        if not rag.is_ready:
            return {"results": [], "message": "RAG non initialisé"}
        results = rag.query(query, n_results=n)
        return {"query": query, "results": results, "count": len(results)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class _AdminAskRequest(_PydanticBaseModel):
    question: str
    conversation_id: Optional[str] = None

@app.post("/api/admin/ask", tags=["Admin"])
async def admin_ask(
    body: _AdminAskRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Invoke le LangGraph AdminAgent complet (FAQ + doc + suivi + reclamation)."""
    user = await get_current_user(authorization, db)
    question = body.question.strip()
    conversation_id = body.conversation_id or f"admin_{user.id}"
    if not question:
        raise HTTPException(status_code=400, detail="question required")

    try:
        from backend.agents.admin_agent import get_admin_agent
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        user_context = {
            "user_id":         user.id,
            "full_name":       user.full_name or user.username,
            "first_name":      user.first_name or (user.full_name or "").split()[0],
            "last_name":       user.last_name  or (" ".join((user.full_name or "").split()[1:]) or ""),
            "username":        user.username,
            "email":           user.email,
            "student_card_id": getattr(profile, "student_card_id", None) or "",
            "major":           getattr(profile, "major", None) or "Genie Informatique",
            "year":            getattr(profile, "year", None) or 3,
            "university":      getattr(profile, "university", None) or "ENIAD Berkane",
            "phone":           getattr(profile, "phone", None) or "",
        }
        agent = get_admin_agent()
        result = await agent.process(
            user_message=question,
            user_id=user.id,
            user_context=user_context,
            conversation_id=str(conversation_id),
        )

        # Attach real PDF bytes when a document was generated
        pdf_base64 = None
        doc_id = result.get("doc_id")
        if doc_id:
            try:
                import base64 as _b64
                from backend.agents.documents_agent import get_documents_agent
                path = get_documents_agent().get_path(doc_id)
                if path:
                    with open(path, "rb") as _f:
                        pdf_base64 = _b64.b64encode(_f.read()).decode("utf-8")
            except Exception as _pdf_err:
                logger.warning(f"Could not attach PDF to agent response: {_pdf_err}")

        return {
            "question":   question,
            "response":   result.get("response", ""),
            "doc_id":     doc_id,
            "pdf_base64": pdf_base64,
            "request_id": result.get("request_id"),
            "ticket_id":  result.get("ticket_id"),
            "agent":      "Agent Admin ReAct LangGraph",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Demandes administratives ──────────────────────────────────────────────────

class _AdminRequestCreate(_PydanticBaseModel):
    request_type: str
    description: Optional[str] = None

@app.post("/api/admin/requests", tags=["Admin"])
async def create_admin_request(
    body: _AdminRequestCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Crée une demande administrative et génère le PDF si possible."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    doc_id = None
    try:
        from backend.agents.documents_agent import get_documents_agent
        _full_name = user.full_name or user.username or ""
        _parts = _full_name.split()
        user_data = {
            "full_name":       _full_name,
            "first_name":      getattr(user, "first_name", None) or (_parts[0] if _parts else ""),
            "last_name":       getattr(user, "last_name",  None) or (" ".join(_parts[1:]) if len(_parts) > 1 else ""),
            "student_id":      str(user.id),
            "student_card_id": (getattr(profile, "student_card_id", None) or str(user.id)) if profile else str(user.id),
            "email":           user.email or "",
            "major":           (getattr(profile, "major",  None) or "Genie Informatique") if profile else "Genie Informatique",
            "year":            (getattr(profile, "year",   None) or 3) if profile else 3,
            "phone":           (getattr(profile, "phone",  None) or "") if profile else "",
            "description":     body.description or "",
        }
        doc_id, _ = get_documents_agent().generate(body.request_type, user_data)
    except Exception:
        pass

    import uuid as _uuid2
    req = AdminRequest(
        id=str(_uuid2.uuid4()),
        user_id=user.id,
        request_type=body.request_type,
        status="validated" if doc_id else "pending",
        description=body.description,
        doc_id=doc_id,
    )
    db.add(req)
    db.commit()
    db.refresh(req)

    return {
        "id": req.id,
        "request_type": req.request_type,
        "status": req.status,
        "doc_id": req.doc_id,
        "created_at": req.created_at.isoformat(),
    }

@app.get("/api/admin/requests", tags=["Admin"])
async def list_admin_requests(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Liste toutes les demandes administratives de l'étudiant connecté."""
    user = await get_current_user(authorization, db)
    items = (
        db.query(AdminRequest)
        .filter(AdminRequest.user_id == user.id)
        .order_by(AdminRequest.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": r.id, "request_type": r.request_type, "status": r.status,
            "doc_id": r.doc_id, "description": r.description,
            "created_at": r.created_at.isoformat(),
        }
        for r in items
    ]

@app.get("/api/admin/requests/{request_id}", tags=["Admin"])
async def get_admin_request(
    request_id: str,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user = await get_current_user(authorization, db)
    req = db.query(AdminRequest).filter(
        AdminRequest.id == request_id, AdminRequest.user_id == user.id
    ).first()
    if not req:
        raise HTTPException(status_code=404, detail="Demande non trouvée")
    return {
        "id": req.id, "request_type": req.request_type, "status": req.status,
        "doc_id": req.doc_id, "description": req.description,
        "created_at": req.created_at.isoformat(),
    }


# ── Réclamations ──────────────────────────────────────────────────────────────

class _ComplaintCreate(_PydanticBaseModel):
    category: str
    description: str

@app.post("/api/admin/complaints", tags=["Admin"])
async def create_complaint(
    body: _ComplaintCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Crée un ticket de réclamation avec numéro unique."""
    user = await get_current_user(authorization, db)
    count = db.query(Complaint).count() + 1
    ticket_id = f"COMP-{datetime.utcnow().year}-{count:05d}"
    complaint = Complaint(
        id=ticket_id,
        user_id=user.id,
        category=body.category,
        description=body.description,
        status="open",
    )
    db.add(complaint)
    db.commit()
    return {
        "id": ticket_id, "category": body.category,
        "status": "open", "created_at": complaint.created_at.isoformat(),
    }

@app.get("/api/admin/complaints", tags=["Admin"])
async def list_complaints(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    user = await get_current_user(authorization, db)
    items = (
        db.query(Complaint)
        .filter(Complaint.user_id == user.id)
        .order_by(Complaint.created_at.desc())
        .limit(20)
        .all()
    )
    return [
        {
            "id": c.id, "category": c.category, "description": c.description,
            "status": c.status, "created_at": c.created_at.isoformat(),
        }
        for c in items
    ]

# ==================== DOCUMENTS ROUTES ====================

import base64 as _base64

class _DocumentRequest(_PydanticBaseModel):
    doc_type: str
    description: Optional[str] = None
    # Convention de stage — company / internship fields
    entreprise: Optional[str] = None
    adresse_entreprise: Optional[str] = None
    tuteur: Optional[str] = None
    poste: Optional[str] = None
    date_debut: Optional[str] = None
    date_fin: Optional[str] = None

@app.post("/api/documents/generate", tags=["Documents"])
async def generate_document(
    req: _DocumentRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Generate a PDF administrative document for the authenticated user."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    full_name = user.full_name or user.username or ""
    name_parts = full_name.split()
    first_name = getattr(user, "first_name", None) or (name_parts[0] if name_parts else "")
    last_name  = getattr(user, "last_name",  None) or (" ".join(name_parts[1:]) if len(name_parts) > 1 else "")

    user_data = {
        "full_name":       full_name,
        "first_name":      first_name,
        "last_name":       last_name,
        "student_id":      str(user.id),
        "student_card_id": (getattr(profile, "student_card_id", None) or str(user.id)) if profile else str(user.id),
        "email":           user.email or "",
        "major":           (getattr(profile, "major", None) or "Genie Informatique") if profile else "Genie Informatique",
        "year":            (getattr(profile, "year",  None) or 3) if profile else 3,
        "phone":           (getattr(profile, "phone", None) or "") if profile else "",
        "description":     req.description or "",
        # Convention de stage fields — filled in or left blank for manual completion
        "entreprise":          req.entreprise or "________________",
        "adresse_entreprise":  req.adresse_entreprise or "________________",
        "tuteur":              req.tuteur or "________________",
        "poste":               req.poste or "Stage de fin d'etudes",
        "date_debut":          req.date_debut or "________________",
        "date_fin":            req.date_fin or "________________",
    }

    # For releve de notes, pull real exam grades
    if any(k in req.doc_type.lower() for k in ("releve", "notes")):
        try:
            exams = db.query(Exam).filter(
                Exam.user_id == user.id, Exam.status == "completed"
            ).all()
            user_data["grades"] = [
                {
                    "matiere": e.subject or e.title,
                    "coefficient": 3,
                    "note": round((e.score / e.total_points) * 20, 2),
                }
                for e in exams
                if e.score is not None and e.total_points
            ]
        except Exception:
            user_data["grades"] = []

    try:
        import asyncio
        from functools import partial
        from backend.agents.documents_agent import get_documents_agent
        agent = get_documents_agent()
        loop = asyncio.get_event_loop()
        doc_id, pdf_bytes = await loop.run_in_executor(
            None, partial(agent.generate, req.doc_type, user_data)
        )
        pdf_b64 = _base64.b64encode(pdf_bytes).decode("utf-8")
        return {
            "doc_id": doc_id,
            "doc_type": req.doc_type,
            "pdf_base64": pdf_b64,
            "generated_at": datetime.utcnow().isoformat(),
            "message": "Document genere avec succes",
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur generation PDF: {str(e)}")

@app.get("/api/documents/download/{doc_id}", tags=["Documents"])
async def download_document(
    doc_id: str,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Download a previously generated PDF document."""
    await get_current_user(authorization, db)
    try:
        from backend.agents.documents_agent import get_documents_agent
        from fastapi.responses import FileResponse
        agent = get_documents_agent()
        path = agent.get_path(doc_id)
        if not path:
            raise HTTPException(status_code=404, detail="Document not found or expired")
        filename = f"document_{doc_id[:8]}.pdf"
        return FileResponse(path, media_type="application/pdf", filename=filename)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# ==================== ERROR HANDLERS ====================

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "status_code": exc.status_code,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

from fastapi.exceptions import RequestValidationError

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    errors = exc.errors()
    detail = "; ".join(
        f"{' -> '.join(str(l) for l in e['loc'])}: {e['msg']}"
        for e in errors
    )
    return JSONResponse(
        status_code=422,
        content={
            "detail": f"Donnees invalides: {detail}",
            "status_code": 422,
            "timestamp": datetime.utcnow().isoformat()
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "backend.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
