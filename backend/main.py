from fastapi import FastAPI, Depends, HTTPException, status, Request, Header, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Optional
import asyncio

from backend.config import get_settings
from backend.database import get_db, init_db, close_db
from backend.models import User, UserProfile, Message, Plan, Event, Exam, Memory, AdminRequest, ExamSchedule, CourseDocument
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
    _migrate_profile_columns()
    _seed_demo_data()
    # Indexer la base de connaissances orientation dans ChromaDB (une seule fois)
    try:
        from backend.agents.orientation_agent import index_orientation_knowledge
        import asyncio
        loop = asyncio.get_event_loop()
        await loop.run_in_executor(None, index_orientation_knowledge)
    except Exception as _ori_err:
        import logging as _lg
        _lg.getLogger(__name__).warning(f"Orientation KB indexation skipped: {_ori_err}")


def _migrate_profile_columns():
    """Add new UserProfile columns if they don't exist yet (safe for existing DBs)."""
    try:
        from backend.database import engine
        from sqlalchemy import text
        with engine.connect() as conn:
            rows = conn.execute(text("PRAGMA table_info(user_profiles)")).fetchall()
            existing = {row[1] for row in rows}
            for col, definition in [
                ("cne",            "TEXT"),
                ("cin",            "TEXT"),
                ("date_naissance", "TEXT"),
            ]:
                if col not in existing:
                    conn.execute(text(f"ALTER TABLE user_profiles ADD COLUMN {col} {definition}"))
            conn.commit()
    except Exception as _mig_err:
        import logging as _lg
        _lg.getLogger(__name__).warning(f"Profile column migration skipped: {_mig_err}")

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

# ==================== MODULES KNOWLEDGE BASE ====================

_DAY_ORDER = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi"]


def _module_code_from_name(nom: str) -> str:
    """Generate a short uppercase code from a module name."""
    stop = {"et", "de", "du", "des", "le", "la", "les", "en", "au", "par", "ou", "un", "une", "l", "d", "a"}
    parts = nom.replace("'", " ").replace("-", " ").replace("(", " ").replace(")", " ").split()
    abbr = "".join(w[:3].upper() for w in parts if w.lower() not in stop and w.isalpha())
    return abbr[:8] or "MOD"


def _extract_modules_from_result(result: dict, has_exam: bool = True) -> list[dict]:
    """Flatten a planning result dict into a list of module dicts ordered by day."""
    planning_data = result.get("planning", {})
    modules: list[dict] = []
    seen: set[str] = set()
    for jour in _DAY_ORDER:
        for creneau, info in (planning_data.get(jour) or {}).items():
            nom = info["module"]
            if nom not in seen:
                seen.add(nom)
                modules.append({
                    "nom": nom,
                    "code": _module_code_from_name(nom),
                    "coefficient": 1.0,
                    "has_exam": has_exam,
                    "exam_jour": jour if has_exam else None,
                    "exam_creneau": creneau if has_exam else None,
                    "exam_salle": info.get("salle") if has_exam else None,
                    "exam_coordonnateur": info.get("coordonnateur") if has_exam else None,
                })
    return modules


def _get_modules_for_student(major: str, year: int, semestre_override: str | None = None) -> dict:
    """Return the module list for a student, sourced from the official exam planning."""
    from backend.data.planning_examens import get_planning_for_filiere, SESSION

    major_lower = (major or "").lower()

    # Determine the semestre
    if semestre_override:
        sem = semestre_override.upper()
    elif any(k in major_lower for k in ["epsi", "préparatoire", "preparatoire"]):
        sem = "S2"
    else:
        # In ENIAD Berkane's post-EPSI engineering cycle:
        # year 1-2  → S6  (spring semester of 2nd engineering year)
        # year 3+   → S8  (spring semester of 3rd/final engineering year)
        sem = "S8" if year >= 3 else "S6"

    result = get_planning_for_filiere(major, sem)
    if not result and not semestre_override:
        # Try the other semestre as fallback
        alt = "S6" if sem == "S8" else "S8"
        result = get_planning_for_filiere(major, alt)
        if result:
            sem = alt

    if result:
        modules = _extract_modules_from_result(result, has_exam=True)
        return {
            "filiere": result["filiere"],
            "semestre": result["semestre"],
            "planning_key": result.get("key", ""),
            "session": SESSION,
            "niveau": year,
            "modules": modules,
            "total_examens": len(modules),
            "source": "planning_officiel",
        }

    # Filière not in official planning — return empty list with info
    return {
        "filiere": major or "Non renseignée",
        "semestre": sem,
        "planning_key": "",
        "session": SESSION,
        "niveau": year,
        "modules": [],
        "total_examens": 0,
        "source": "non_disponible",
        "message": "Votre filière n'est pas couverte par le planning officiel de cette session.",
    }


@app.get("/api/user/modules", tags=["Exams"])
async def get_user_modules(
    semestre: Optional[str] = None,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Retourner les modules de l'étudiant avec leurs créneaux d'examen planifiés."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    major = getattr(profile, "major", None) or ""
    year = int(getattr(profile, "year", None) or 1)

    return _get_modules_for_student(major, year, semestre_override=semestre)


# ── PDF Q&A endpoint ──────────────────────────────────────────────────────────

class _CourseAskRequest(_PydanticBaseModel):
    question: str
    type: Optional[str] = "question"  # resume | notions | examen | question


@app.post("/api/exams/courses/{doc_id}/ask", tags=["Exams"])
async def ask_course_pdf(
    doc_id: int,
    body: _CourseAskRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Répondre à une question IA basée sur le contenu d'un cours importé."""
    user = await get_current_user(authorization, db)
    doc = db.query(CourseDocument).filter(
        CourseDocument.id == doc_id, CourseDocument.user_id == user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")

    contenu = (doc.contenu or "")[:8000]
    ask_type = body.type or "question"
    question = body.question

    if ask_type == "resume":
        system_msg = "Tu es un assistant pédagogique expert. Génère un résumé structuré et complet du cours."
        user_msg = (
            f"Cours : {doc.titre or doc.matiere}\n\nContenu :\n{contenu}\n\n"
            "Génère un résumé structuré avec : introduction, points principaux numérotés, concepts clés, et conclusion."
        )
    elif ask_type == "notions":
        system_msg = "Tu es un assistant pédagogique. Identifie les notions clés susceptibles d'apparaître à l'examen."
        user_msg = (
            f"Cours : {doc.titre or doc.matiere}\n\nContenu :\n{contenu}\n\n"
            "Liste les notions importantes, définitions, formules et points d'examen potentiels de façon structurée."
        )
    elif ask_type == "examen":
        system_msg = "Tu es un professeur qui génère des questions d'examen variées avec réponses détaillées."
        user_msg = (
            f"Cours : {doc.titre or doc.matiere}\n\nContenu :\n{contenu}\n\n"
            "Génère 5 questions d'examen variées (QCM, ouvertes, exercices) couvrant les points importants, avec les réponses."
        )
    else:
        system_msg = "Tu es un assistant pédagogique qui répond aux questions sur un cours de manière claire et structurée."
        user_msg = (
            f"Cours : {doc.titre or doc.matiere}\n\nContenu :\n{contenu}\n\n"
            f"Question : {question}\n\nRéponds de manière précise et pédagogique."
        )

    try:
        from backend.agents.orchestrator import get_llm
        from langchain_core.messages import SystemMessage as _SMsg, HumanMessage as _HMsg
        llm = get_llm()
        resp = llm.invoke([_SMsg(content=system_msg), _HMsg(content=user_msg)])
        answer = resp.content.strip()

        if ask_type == "resume" and not doc.resume:
            doc.resume = answer
            db.commit()

        return {"question": question, "type": ask_type, "response": answer, "matiere": doc.matiere}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur IA : {e}")


# ==================== EXAM SCHEDULE ROUTES ====================

class _ExamScheduleCreate(_PydanticBaseModel):
    matiere: str
    date_examen: datetime
    semestre: Optional[str] = None
    salle: Optional[str] = None
    coefficient: float = 1.0
    notes: Optional[str] = None


@app.post("/api/exams/schedule", tags=["Exams"])
async def create_exam_schedule(
    body: _ExamScheduleCreate,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Enregistrer un examen officiel à venir."""
    user = await get_current_user(authorization, db)
    entry = ExamSchedule(
        user_id=user.id,
        matiere=body.matiere,
        date_examen=body.date_examen,
        semestre=body.semestre,
        salle=body.salle,
        coefficient=body.coefficient,
        notes=body.notes,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return {
        "id": entry.id,
        "matiere": entry.matiere,
        "date_examen": entry.date_examen.isoformat(),
        "semestre": entry.semestre,
        "salle": entry.salle,
        "coefficient": entry.coefficient,
        "notes": entry.notes,
    }


@app.get("/api/exams/schedule", tags=["Exams"])
async def get_exam_schedule(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Obtenir le planning des examens officiels à venir."""
    user = await get_current_user(authorization, db)
    now = datetime.utcnow()
    entries = (
        db.query(ExamSchedule)
        .filter(ExamSchedule.user_id == user.id, ExamSchedule.date_examen >= now)
        .order_by(ExamSchedule.date_examen)
        .all()
    )
    result = []
    for e in entries:
        days = (e.date_examen - now).days
        urgency = "URGENT" if days <= 3 else ("Proche" if days <= 7 else "Normal")
        result.append({
            "id": e.id,
            "matiere": e.matiere,
            "date_examen": e.date_examen.isoformat(),
            "semestre": e.semestre,
            "salle": e.salle,
            "coefficient": e.coefficient,
            "notes": e.notes,
            "jours_restants": days,
            "urgence": urgency,
        })
    return result


@app.delete("/api/exams/schedule/{entry_id}", tags=["Exams"])
async def delete_exam_schedule(
    entry_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Supprimer un examen du planning."""
    user = await get_current_user(authorization, db)
    entry = db.query(ExamSchedule).filter(
        ExamSchedule.id == entry_id, ExamSchedule.user_id == user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Examen non trouvé")
    db.delete(entry)
    db.commit()
    return {"message": "Examen supprimé"}


@app.get("/api/exams/official-schedule", tags=["Exams"])
async def get_official_exam_schedule(
    filiere: Optional[str] = None,
    semestre: Optional[str] = None,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Retourner le planning officiel des examens (PDF extrait) pour la filière de l'étudiant."""
    user = await get_current_user(authorization, db)
    from backend.data.planning_examens import get_planning_for_filiere, search_module_in_planning, SESSION

    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    major = filiere or getattr(profile, "major", None) or ""
    result = get_planning_for_filiere(major, semestre)
    if not result:
        # Return all filieres list so frontend can show a picker
        from backend.data.planning_examens import FILIERES_INFO
        return {
            "session": SESSION,
            "filiere": major,
            "planning": {},
            "available_filieres": [
                {"cle": k, "nom": v[0], "semestre": v[1]}
                for k, v in FILIERES_INFO.items()
            ],
            "message": "Filière non trouvée, choisissez parmi les filières disponibles",
        }
    return {"session": SESSION, **result}


@app.get("/api/exams/official-schedule/search", tags=["Exams"])
async def search_official_schedule(
    q: str,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Rechercher un module dans le planning officiel."""
    await get_current_user(authorization, db)
    from backend.data.planning_examens import search_module_in_planning
    results = search_module_in_planning(q)
    return {"query": q, "results": results}


# ==================== COURSE DOCUMENT ROUTES ====================

from fastapi import Form, UploadFile, File


@app.post("/api/exams/courses/upload", tags=["Exams"])
async def upload_course_pdf(
    matiere: str = Form(...),
    titre: str = Form(""),
    file: UploadFile = File(...),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Uploader un PDF de cours. Le texte est extrait puis stocké pour analyse IA."""
    user = await get_current_user(authorization, db)

    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")

    pdf_bytes = await file.read()
    if len(pdf_bytes) > 10 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 10 Mo)")

    # Extract text with pdfplumber
    try:
        import pdfplumber, io
        contenu = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    contenu += text + "\n"
        contenu = contenu.strip()
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Impossible d'extraire le texte du PDF: {e}")

    if not contenu:
        raise HTTPException(status_code=422, detail="Le PDF ne contient pas de texte extractible")

    # Store in CourseDocument
    doc = CourseDocument(
        user_id=user.id,
        matiere=matiere,
        titre=titre or file.filename,
        contenu=contenu,
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)

    return {
        "id": doc.id,
        "matiere": doc.matiere,
        "titre": doc.titre,
        "chars": len(contenu),
        "created_at": doc.created_at.isoformat(),
        "message": f"Cours '{doc.titre}' importé avec succès ({len(contenu)} caractères extraits).",
    }


@app.get("/api/exams/courses", tags=["Exams"])
async def list_course_documents(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Lister les cours importés par l'étudiant."""
    user = await get_current_user(authorization, db)
    docs = (
        db.query(CourseDocument)
        .filter(CourseDocument.user_id == user.id)
        .order_by(CourseDocument.created_at.desc())
        .all()
    )
    return [
        {
            "id": d.id,
            "matiere": d.matiere,
            "titre": d.titre,
            "chars": len(d.contenu) if d.contenu else 0,
            "has_resume": bool(d.resume),
            "has_notions": bool(d.notions_cles),
            "created_at": d.created_at.isoformat(),
        }
        for d in docs
    ]


@app.delete("/api/exams/courses/{doc_id}", tags=["Exams"])
async def delete_course_document(
    doc_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Supprimer un cours importé."""
    user = await get_current_user(authorization, db)
    doc = db.query(CourseDocument).filter(
        CourseDocument.id == doc_id, CourseDocument.user_id == user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    db.delete(doc)
    db.commit()
    return {"message": "Cours supprimé"}


@app.get("/api/exams/courses/{doc_id}", tags=["Exams"])
async def get_course_document(
    doc_id: int,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Obtenir le contenu complet d'un cours (texte + résumé + notions clés)."""
    user = await get_current_user(authorization, db)
    doc = db.query(CourseDocument).filter(
        CourseDocument.id == doc_id, CourseDocument.user_id == user.id
    ).first()
    if not doc:
        raise HTTPException(status_code=404, detail="Document non trouvé")
    return {
        "id": doc.id,
        "matiere": doc.matiere,
        "titre": doc.titre,
        "contenu": doc.contenu,
        "resume": doc.resume,
        "notions_cles": doc.notions_cles,
        "created_at": doc.created_at.isoformat(),
        "updated_at": doc.updated_at.isoformat(),
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

def _format_support_response(info: dict, nom: str = "l'étudiant") -> str:
    """Formate la réponse guide administrative à partir d'une entrée ADMIN_SUPPORT_MAP."""
    steps = "\n".join(f"• {s}" for s in info.get("process", []))
    docs  = "\n".join(f"• {d}" for d in info.get("documents_requis", []))
    contact_lines = [f"• {info['service']}"]
    contact_lines.append(f"• Responsable : {info['responsable']}")
    if info.get("bureau"):
        contact_lines.append(f"• Bureau : {info['bureau']}")
    if info.get("email"):
        contact_lines.append(f"• Email : {info['email']}")
    if info.get("telephone"):
        contact_lines.append(f"• Téléphone : {info['telephone']}")
    if info.get("horaires"):
        contact_lines.append(f"• Horaires : {info['horaires']}")
    contact_block = "\n".join(contact_lines)
    return (
        f"**Sujet : {info['title']}**\n\n"
        f"**Étapes :**\n{steps}\n\n"
        + (f"**Documents requis :**\n{docs}\n\n" if docs else "")
        + f"**Service responsable :**\n{contact_block}\n\n"
        f"⏱ Délai estimé : {info.get('delai_estime', 'À confirmer avec le service')}\n"
        f"✅ Résultat attendu : {info.get('resultat_attendu', '')}"
    )


def _direct_classify_message(text: str) -> str | None:
    """Retourne la clé ADMIN_SUPPORT_MAP si le message correspond à une situation connue, sinon None."""
    from backend.agents.admin_agent import ADMIN_SUPPORT_MAP
    t = text.lower()
    scores = {key: sum(1 for kw in info.get("keywords", []) if kw in t)
              for key, info in ADMIN_SUPPORT_MAP.items()}
    best = max(scores, key=lambda k: scores[k])
    if scores[best] > 0:
        return best
    # Simple fallback words
    _fallback = [
        (["carte", "perdu", "perdue", "duplicata"], "carte_perdue"),
        (["filiere", "filière", "transfert filiere"], "changement_filiere"),
        (["attestation"], "attestation"),
        (["releve", "bulletin"], "releve_notes"),
        (["probleme note", "erreur note", "ma note", "contestation"], "probleme_note"),
        (["absent", "absence", "justificatif", "rate examen"], "absence_examen"),
        (["pfe", "pfa", "fin d'etude", "memoire"], "stage_pfa_pfe"),
        (["convention", "stage"], "convention_stage"),
        (["plateforme", "moodle", "ent", "portail"], "acces_plateforme"),
        (["mot de passe", "password", "mdp", "reinitialisation"], "reinitialisation_mdp"),
        (["wifi", "wi-fi", "connexion", "reseau", "internet"], "wifi"),
        (["bourse", "aide financiere", "aide sociale"], "bourse"),
        (["evenement", "événement", "club", "participer", "hackathon", "conference"], "participation_evenement"),
        (["certificat"], "certificat"),
        (["diplome", "diplôme", "retrait"], "retrait_diplome"),
    ]
    for words, key in _fallback:
        if any(w in t for w in words):
            return key
    return None


# Keywords that indicate a document generation request needing the LLM agent
_DOC_GEN_KEYWORDS = [
    "genere", "générer", "génère",
    "attestation de scolarite", "attestation scolarite",
    "convention de stage",
    "reglement de l'ecole", "reglement ecole", "reglement",
    "télécharger", "telecharger", "pdf",
]


# ── Attestation: required fields and their display labels ─────────────────────
_ATT_REQUIRED_FIELDS: dict[str, str] = {
    "major":          "Filière d'études",
    "year":           "Niveau (année)",
    "cne":            "Code Massar / CNE",
    "date_naissance": "Date de naissance",
}


@app.get("/api/admin/attestation/prefill", tags=["Admin"])
async def attestation_prefill(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Return the student's available profile data and which required fields are missing."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    def _g(attr, fallback=""):
        return getattr(profile, attr, None) or fallback if profile else fallback

    data = {
        "full_name":      user.full_name or user.username or "",
        "first_name":     user.first_name or "",
        "last_name":      user.last_name  or "",
        "email":          user.email or "",
        "major":          _g("major"),
        "year":           _g("year", 0),
        "cne":            _g("cne"),
        "cin":            _g("cin"),
        "date_naissance": _g("date_naissance"),
        "student_card_id": _g("student_card_id"),
    }

    missing = {
        k: label
        for k, label in _ATT_REQUIRED_FIELDS.items()
        if not data.get(k)
    }

    return {
        "profile":          data,
        "missing_fields":   missing,
        "can_generate_now": len(missing) == 0,
    }


class _AttestationGenerateRequest(_PydanticBaseModel):
    extra_fields: Optional[dict] = {}


@app.post("/api/admin/attestation/generate", tags=["Admin"])
async def attestation_generate(
    body: _AttestationGenerateRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Generate the attestation PDF, merging profile data with any extra fields provided."""
    import base64 as _b64, uuid as _uuid
    from backend.agents.documents_agent import get_documents_agent
    from datetime import datetime as _dt

    user    = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    extra   = body.extra_fields or {}

    def _g(attr, fallback=""):
        return getattr(profile, attr, None) or fallback if profile else fallback

    # Persist any newly provided fields back to the profile
    if profile and extra:
        for field in ("major", "year", "cne", "cin", "date_naissance", "student_card_id"):
            if field in extra and extra[field]:
                try:
                    val = int(extra[field]) if field == "year" else str(extra[field])
                    setattr(profile, field, val)
                except (ValueError, TypeError):
                    pass
        db.commit()

    # Build complete user_data (extra overrides profile)
    def _pick(key, fallback=""):
        return extra.get(key) or _g(key, fallback)

    now = _dt.now()
    yr  = now.year if now.month >= 9 else now.year - 1
    annee_univ = f"{yr}/{yr + 1}"

    user_data = {
        "full_name":          user.full_name or user.username or "",
        "first_name":         user.first_name or "",
        "last_name":          user.last_name  or "",
        "email":              user.email or "",
        "major":              _pick("major"),
        "year":               int(_pick("year", 0) or 0),
        "cne":                _pick("cne"),
        "cin":                _pick("cin"),
        "date_naissance":     _pick("date_naissance"),
        "student_card_id":    _pick("student_card_id", str(user.id)),
        "annee_universitaire": annee_univ,
    }

    # Validate mandatory fields
    missing = [v for k, v in _ATT_REQUIRED_FIELDS.items() if not user_data.get(k)]
    if missing:
        raise HTTPException(400, detail=f"Informations manquantes : {', '.join(missing)}")

    doc_id, pdf_bytes = get_documents_agent().generate("Attestation de scolarite", user_data)

    req_id = str(_uuid.uuid4())
    db.add(AdminRequest(
        id=req_id, user_id=user.id,
        request_type="Attestation de scolarite",
        status="validated",
        description="Générée automatiquement depuis le profil étudiant",
        doc_id=doc_id,
    ))
    db.commit()

    _levels = {1: "1ère", 2: "2ème", 3: "3ème", 4: "4ème", 5: "5ème"}
    niveau = _levels.get(user_data["year"], f"{user_data['year']}ème")
    nom    = user.full_name or user.username or "étudiant"

    return {
        "doc_id":     doc_id,
        "pdf_base64": _b64.b64encode(pdf_bytes).decode("utf-8"),
        "request_id": req_id,
        "message": (
            f"Votre attestation de scolarité a été générée avec succès, {nom} !\n\n"
            f"Elle certifie votre inscription en **{user_data['major']}** "
            f"({niveau} année) pour l'année universitaire **{annee_univ}**.\n\n"
            f"Vous pouvez la télécharger depuis l'onglet **Documents**."
        ),
    }


@app.post("/api/admin/ask", tags=["Admin"])
async def admin_ask(
    body: _AdminAskRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
):
    """Guide administratif : oriente l'étudiant ou génère un document officiel."""
    user = await get_current_user(authorization, db)
    question = body.question.strip()
    conversation_id = body.conversation_id or f"admin_{user.id}"
    if not question:
        raise HTTPException(status_code=400, detail="question required")

    nom = user.full_name or user.username or "étudiant"
    q_lower = question.lower()

    # ── Attestation de scolarité: direct generation (no LLM) ─────────────────
    _ATT_TRIGGERS = [
        "attestation", "attestation de scolarite", "attestation scolarite",
        "justificatif scolarite", "justificatif d inscription",
        "preuve inscription", "preuve de scolarite",
    ]
    _is_attestation = (
        any(kw in q_lower for kw in _ATT_TRIGGERS)
        and "convention" not in q_lower
        and "stage" not in q_lower
        and "reglement" not in q_lower
    )
    if _is_attestation:
        try:
            import base64 as _b64, uuid as _uuid
            from backend.agents.documents_agent import get_documents_agent
            from datetime import datetime as _dt

            profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

            def _g(attr, fallback=""):
                return getattr(profile, attr, None) or fallback if profile else fallback

            now = _dt.now()
            yr_start = now.year if now.month >= 9 else now.year - 1
            annee_univ = f"{yr_start}-{yr_start + 1}"

            user_data = {
                "full_name":          user.full_name or user.username or "",
                "first_name":         user.first_name or "",
                "last_name":          user.last_name  or "",
                "email":              user.email or "",
                "phone":              _g("phone"),
                "major":              _g("major", "Non renseignee"),
                "year":               _g("year", 0),
                "student_card_id":    _g("student_card_id", str(user.id)),
                "cne":                _g("cne"),
                "cin":                _g("cin"),
                "date_naissance":     _g("date_naissance"),
                "annee_universitaire": annee_univ,
            }

            # Check only truly mandatory fields
            missing = []
            if not user_data["major"] or user_data["major"] == "Non renseignee":
                missing.append("votre **filière** (ex : Intelligence Artificielle, Génie Informatique…)")
            if not user_data["year"]:
                missing.append("votre **niveau** (1ère, 2ème ou 3ème année)")

            if missing:
                return {
                    "question":   question,
                    "response":   (
                        "Pour générer votre attestation de scolarité, j'ai besoin des informations suivantes :\n\n"
                        + "\n".join(f"• {m}" for m in missing)
                        + "\n\nVeuillez compléter votre profil dans les paramètres, ou précisez ces informations ici."
                    ),
                    "doc_id":     None, "pdf_base64": None,
                    "request_id": None, "ticket_id":  None,
                    "agent":      "Guide Admin Direct",
                }

            doc_id, pdf_bytes = get_documents_agent().generate("Attestation de scolarite", user_data)

            req_id = str(_uuid.uuid4())
            req = AdminRequest(
                id=req_id, user_id=user.id,
                request_type="Attestation de scolarite",
                status="validated",
                description="Générée automatiquement depuis le profil étudiant",
                doc_id=doc_id,
            )
            db.add(req)
            db.commit()

            level_labels = {1: "1ère", 2: "2ème", 3: "3ème", 4: "4ème", 5: "5ème"}
            niveau = level_labels.get(int(user_data["year"]) if user_data["year"] else 0, f"{user_data['year']}ème")

            return {
                "question": question,
                "response": (
                    f"Votre **attestation de scolarité** a été générée avec succès, {nom} !\n\n"
                    f"Elle certifie votre inscription en **{user_data['major']}** "
                    f"({niveau} année) pour l'année universitaire **{annee_univ}**.\n\n"
                    f"Vous pouvez la télécharger depuis l'onglet **Documents**."
                ),
                "doc_id":     doc_id,
                "pdf_base64": _b64.b64encode(pdf_bytes).decode("utf-8"),
                "request_id": req_id,
                "ticket_id":  None,
                "agent":      "Guide Admin Direct",
            }
        except Exception as _att_err:
            import logging as _lg
            _lg.getLogger(__name__).error(f"attestation fast-path error: {_att_err}")
            # Fall through to regular paths below

    # ── Règlement de l'école: direct generation (no LLM) ─────────────────────
    _REGL_TRIGGERS = [
        "reglement", "règlement", "reglement interieur", "règlement intérieur",
        "reglement de l'ecole", "règlement de l'école", "reglement ecole",
    ]
    _is_reglement = (
        any(kw in q_lower for kw in _REGL_TRIGGERS)
        and "attestation" not in q_lower
        and "convention" not in q_lower
        and "stage" not in q_lower
    )
    if _is_reglement:
        try:
            import base64 as _b64, uuid as _uuid
            from backend.agents.documents_agent import get_documents_agent

            profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

            def _gr(attr, fallback=""):
                return getattr(profile, attr, None) or fallback if profile else fallback

            user_data = {
                "full_name": user.full_name or user.username or "",
                "cin":       _gr("cin"),
                "year":      _gr("year", ""),
                "major":     _gr("major", ""),
            }

            doc_id, pdf_bytes = get_documents_agent().generate("Reglement de l'ecole", user_data)

            req_id = str(_uuid.uuid4())
            req = AdminRequest(
                id=req_id, user_id=user.id,
                request_type="Reglement de l'ecole",
                status="validated",
                description="Règlement intérieur ENIAD - demandé par l'étudiant",
                doc_id=doc_id,
            )
            db.add(req)
            db.commit()

            return {
                "question": question,
                "response": (
                    f"Voici le **règlement intérieur officiel de l'ENIAD**, {nom} !\n\n"
                    "Ce document contient toutes les règles et dispositions officielles "
                    "de l'école (31 articles). La dernière page comporte un espace pour "
                    "votre signature d'engagement.\n\n"
                    "Vous pouvez le télécharger via le bouton **PDF** ci-dessous ou depuis l'onglet **Documents**."
                ),
                "doc_id":     doc_id,
                "pdf_base64": _b64.b64encode(pdf_bytes).decode("utf-8"),
                "request_id": req_id,
                "ticket_id":  None,
                "agent":      "Guide Admin Direct",
            }
        except Exception as _regl_err:
            import logging as _lg
            _lg.getLogger(__name__).error(f"reglement fast-path error: {_regl_err}")
            # Fall through to regular paths below

    # ── Fast path (wrapped in try so any import error never reaches the client) ─
    try:
        from backend.agents.admin_agent import ADMIN_SUPPORT_MAP, _detect_intent, _build_smart_response
        needs_doc_gen = any(kw in q_lower for kw in _DOC_GEN_KEYWORDS)
        if not needs_doc_gen:
            key = _direct_classify_message(question)
            if key and key in ADMIN_SUPPORT_MAP:
                intent = _detect_intent(question)
                return {
                    "question":   question,
                    "response":   _build_smart_response(ADMIN_SUPPORT_MAP[key], nom, intent, question),
                    "doc_id":     None,
                    "pdf_base64": None,
                    "request_id": None,
                    "ticket_id":  None,
                    "agent":      "Guide Admin Direct",
                }
    except Exception as _fast_err:
        logger.warning(f"admin_ask fast-path error (continuing to slow path): {_fast_err}")
        needs_doc_gen = False  # reset so slow path runs

    # ── Slow path: LLM agent for document generation & complex queries ────────
    try:
        from backend.agents.admin_agent import ADMIN_SUPPORT_MAP, get_admin_agent
        profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
        user_context = {
            "user_id":          user.id,
            "full_name":        user.full_name or user.username,
            "first_name":       user.first_name or (user.full_name or "").split()[0],
            "last_name":        user.last_name  or (" ".join((user.full_name or "").split()[1:]) or ""),
            "username":         user.username,
            "email":            user.email,
            "student_card_id":  getattr(profile, "student_card_id", None) or "",
            "cne":              getattr(profile, "cne", None) or "",
            "cin":              getattr(profile, "cin", None) or "",
            "date_naissance":   getattr(profile, "date_naissance", None) or "",
            "major":            getattr(profile, "major", None) or "Genie Informatique",
            "year":             getattr(profile, "year", None) or 3,
            "university":       getattr(profile, "university", None) or "ENIAD Berkane",
            "phone":            getattr(profile, "phone", None) or "",
        }
        agent = get_admin_agent()
        result = await agent.process(
            user_message=question,
            user_id=user.id,
            user_context=user_context,
            conversation_id=str(conversation_id),
        )

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
        logger.error(f"admin_ask error: {e}")
        # Final fallback: try classification once more
        try:
            from backend.agents.admin_agent import ADMIN_SUPPORT_MAP, _detect_intent, _build_smart_response
            key = _direct_classify_message(question)
            if key and key in ADMIN_SUPPORT_MAP:
                intent = _detect_intent(question)
                return {
                    "question":   question,
                    "response":   _build_smart_response(ADMIN_SUPPORT_MAP[key], nom, intent, question),
                    "doc_id":     None,
                    "pdf_base64": None,
                    "request_id": None,
                    "ticket_id":  None,
                    "agent":      "Guide Admin Direct (fallback)",
                }
        except Exception:
            pass
        return {
            "question":   question,
            "response":   (
                "Je ne peux pas traiter votre demande pour l'instant. "
                "Pour obtenir de l'aide, veuillez contacter directement le secrétariat ENIAD : "
                "scolarite@eniad.ma | +212 5 36 00 10 01 | Bureau A01"
            ),
            "doc_id":     None,
            "pdf_base64": None,
            "request_id": None,
            "ticket_id":  None,
            "agent":      "fallback",
        }


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


# ==================== SUPPORT ADMINISTRATIF INTELLIGENT ====================

class _RecommendationRequest(_PydanticBaseModel):
    prenom:       str
    nom:          str
    cne:          Optional[str] = None
    filiere:      str
    annee:        str
    type_demande: str
    description:  str


# Mapping type_demande Flutter → clé ADMIN_SUPPORT_MAP (15 situations)
_TYPE_DEMANDE_MAP: dict[str, str] = {
    "changement de filière":                        "changement_filiere",
    "changement de filiere":                        "changement_filiere",
    "inscription / réinscription":                  "changement_filiere",
    "inscription / reinscription":                  "changement_filiere",
    "problème sur les notes":                       "probleme_note",
    "probleme sur les notes":                       "probleme_note",
    "réclamation sur un examen":                    "absence_examen",
    "reclamation sur un examen":                    "absence_examen",
    "absence examen":                               "absence_examen",
    "demande de documents (attestation, relevé…)":  "attestation",
    "demande de documents (attestation, releve...)": "attestation",
    "attestation":                                  "attestation",
    "relevé de notes":                              "releve_notes",
    "releve de notes":                              "releve_notes",
    "convention de stage":                          "convention_stage",
    "problème avec un module / dispense":           "probleme_note",
    "probleme avec un module / dispense":           "probleme_note",
    "bourse / aide sociale":                        "bourse",
    "bourse":                                       "bourse",
    "problème technique (compte, wifi…)":           "wifi",
    "probleme technique (compte, wifi...)":         "wifi",
    "wifi":                                         "wifi",
    "mot de passe":                                 "reinitialisation_mdp",
    "réinitialisation mot de passe":                "reinitialisation_mdp",
    "reinitialisation mot de passe":                "reinitialisation_mdp",
    "accès plateforme":                             "acces_plateforme",
    "acces plateforme":                             "acces_plateforme",
    "pfe / mémoire":                                "stage_pfa_pfe",
    "pfe / memoire":                                "stage_pfa_pfe",
    "pfa":                                          "stage_pfa_pfe",
    "pfe":                                          "stage_pfa_pfe",
    "problème administratif général":               "certificat",
    "probleme administratif general":               "certificat",
    "orientation professionnelle":                  "stage_pfa_pfe",
    "diplôme":                                      "retrait_diplome",
    "diplome":                                      "retrait_diplome",
    "retrait diplôme":                              "retrait_diplome",
    "participation événement":                      "participation_evenement",
    "participation evenement":                      "participation_evenement",
    "certificat":                                   "certificat",
}


def _classify_support(type_demande: str, description: str) -> str:
    """Retourne la clé ADMIN_SUPPORT_MAP correspondant au problème étudiant."""
    from backend.agents.admin_agent import ADMIN_SUPPORT_MAP

    # 1. Correspondance directe sur type_demande (normalisé)
    td_norm = type_demande.lower().strip()
    if td_norm in _TYPE_DEMANDE_MAP:
        return _TYPE_DEMANDE_MAP[td_norm]

    # 2. Correspondance partielle sur type_demande
    for label, key in _TYPE_DEMANDE_MAP.items():
        if label in td_norm or td_norm in label:
            return key

    # 3. Scoring par mots-clés sur description + type_demande combinés
    text = f"{type_demande} {description}".lower()
    scores: dict[str, int] = {}
    for key, info in ADMIN_SUPPORT_MAP.items():
        scores[key] = sum(1 for kw in info.get("keywords", []) if kw in text)

    best = max(scores, key=lambda k: scores[k])
    if scores[best] > 0:
        return best

    # 4. Fallback par mots génériques
    if any(w in text for w in ["carte", "perdu", "perdue", "duplicata"]):
        return "carte_perdue"
    if any(w in text for w in ["wifi", "wi-fi", "connexion", "reseau", "internet"]):
        return "wifi"
    if any(w in text for w in ["mot de passe", "password", "mdp", "reinitialisation"]):
        return "reinitialisation_mdp"
    if any(w in text for w in ["plateforme", "moodle", "ent", "portail"]):
        return "acces_plateforme"
    if any(w in text for w in ["pfe", "pfa", "stage fin", "fin d'etude", "memoire"]):
        return "stage_pfa_pfe"
    if any(w in text for w in ["convention", "stage"]):
        return "convention_stage"
    if any(w in text for w in ["attestation", "inscription"]):
        return "attestation"
    if any(w in text for w in ["releve", "bulletin", "notes"]):
        return "releve_notes"
    if any(w in text for w in ["certificat"]):
        return "certificat"
    if any(w in text for w in ["diplome", "diplôme"]):
        return "retrait_diplome"
    if any(w in text for w in ["bourse", "aide", "financier"]):
        return "bourse"
    if any(w in text for w in ["absence", "examen rate", "justificatif"]):
        return "absence_examen"
    if any(w in text for w in ["note", "erreur note", "contestation"]):
        return "probleme_note"
    if any(w in text for w in ["filiere", "changement", "transfert"]):
        return "changement_filiere"
    if any(w in text for w in ["evenement", "club", "participer", "conference"]):
        return "participation_evenement"
    return "attestation"


@app.post("/api/recommendations/generate", tags=["Support Administratif"])
async def generate_recommendations(
    body: _RecommendationRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Support administratif intelligent : identifie le problème et guide l'étudiant étape par étape."""
    await get_current_user(authorization, db)

    from backend.agents.admin_agent import ADMIN_SUPPORT_MAP

    key = _classify_support(body.type_demande, body.description)
    info = ADMIN_SUPPORT_MAP[key]

    desc = (
        f"Votre demande concernant « {body.type_demande} » a été analysée. "
        f"Elle relève du {info['service']} — {info['responsable']}. "
        f"Suivez le processus ci-dessous pour résoudre votre situation rapidement."
    )

    support_card = {
        "titre": info["title"],
        "priorite": info.get("priorite", 2),
        "description": desc,
        "processus": {
            "service":          info["service"],
            "responsable":      info["responsable"],
            "email":            info.get("email", ""),
            "telephone":        info.get("telephone", ""),
            "documents_requis": info.get("documents_requis", []),
            "etapes":           [f"Étape {i+1} : {s}" for i, s in enumerate(info.get("process", []))],
            "delai_estime":     info.get("delai_estime", "À confirmer avec le service"),
            "resultat_attendu": info.get("resultat_attendu", ""),
        },
    }

    return {
        "student": {
            "prenom":       body.prenom,
            "nom":          body.nom,
            "filiere":      body.filiere,
            "annee":        body.annee,
            "type_demande": body.type_demande,
        },
        "recommendations": [support_card],
        "generated_at": datetime.utcnow().isoformat(),
    }


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
    """Generate a PDF administrative document for the authenticated user.

    Only three document types are accepted:
    - 'Attestation de scolarite'
    - 'Convention de stage'
    - "Reglement de l'ecole"
    """
    from backend.agents.documents_agent import ALLOWED_DOC_TYPES, resolve_doc_type

    # ── Whitelist check — reject forbidden types immediately ──────────────────
    try:
        canonical = resolve_doc_type(req.doc_type)
    except ValueError:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Type de document '{req.doc_type}' non autorise. "
                f"Types valides: {', '.join(ALLOWED_DOC_TYPES)}"
            ),
        )

    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    full_name = user.full_name or user.username or ""
    name_parts = full_name.split()
    first_name = getattr(user, "first_name", None) or (name_parts[0] if name_parts else "")
    last_name  = getattr(user, "last_name",  None) or (" ".join(name_parts[1:]) if len(name_parts) > 1 else "")

    # ── Build doc-specific user_data — no cross-module data ──────────────────
    user_data: dict = {
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
    }

    # Convention de stage: internship fields are added only for this type
    if canonical == "Convention de stage":
        user_data.update({
            "entreprise":         req.entreprise or "________________",
            "adresse_entreprise": req.adresse_entreprise or "________________",
            "tuteur":             req.tuteur or "________________",
            "poste":              req.poste or "Stage de fin d'etudes",
            "date_debut":         req.date_debut or "________________",
            "date_fin":           req.date_fin or "________________",
        })
    # Attestation and Reglement receive no extra fields — generators handle that.

    try:
        from functools import partial
        from backend.agents.documents_agent import get_documents_agent
        agent = get_documents_agent()
        loop = asyncio.get_event_loop()
        doc_id, pdf_bytes = await loop.run_in_executor(
            None, partial(agent.generate, canonical, user_data)
        )
        pdf_b64 = _base64.b64encode(pdf_bytes).decode("utf-8")
        return {
            "doc_id":       doc_id,
            "doc_type":     canonical,
            "pdf_base64":   pdf_b64,
            "generated_at": datetime.utcnow().isoformat(),
            "message":      "Document genere avec succes",
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

# ==================== ORIENTATION ROUTES ====================

class _LmGenerateRequest(_PydanticBaseModel):
    poste: str
    entreprise: str
    type_lm: Optional[str] = "startup"   # startup | multinational
    competences: Optional[str] = None
    projets: Optional[str] = None

@app.post("/api/orientation/analyze-cv", tags=["Orientation"])
async def analyze_cv(
    cv_file: UploadFile = File(...),
    poste_cible: str = Form(""),
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Analyser un CV (PDF uploadé) et fournir des recommandations personnalisées."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()

    if not cv_file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Seuls les fichiers PDF sont acceptés")

    pdf_bytes = await cv_file.read()
    if len(pdf_bytes) > 5 * 1024 * 1024:
        raise HTTPException(status_code=400, detail="Fichier trop volumineux (max 5 Mo)")

    try:
        import pdfplumber, io
        cv_text = ""
        with pdfplumber.open(io.BytesIO(pdf_bytes)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if text:
                    cv_text += text + "\n"
        cv_text = cv_text.strip()
    except Exception as e:
        raise HTTPException(status_code=422, detail=f"Impossible d'extraire le texte du PDF : {e}")

    if not cv_text:
        raise HTTPException(
            status_code=422,
            detail="Le PDF ne contient pas de texte extractible. Assurez-vous que votre CV est un PDF avec du texte (pas une image scannée).",
        )

    filiere = getattr(profile, "major", None) or "Informatique"
    annee = getattr(profile, "year", None) or 3
    nom = user.full_name or user.username or "étudiant"
    poste_context = f"pour le poste de '{poste_cible}'" if poste_cible else "pour des stages ou emplois en informatique"
    prompt_system = (
        "Tu es un expert en recrutement spécialisé pour les ingénieurs informatiques au Maroc. "
        "Tu analyses des CVs d'étudiants de l'ENIAD Berkane et fournis des recommandations précises, "
        "constructives et adaptées au marché marocain."
    )
    prompt_user = (
        f"Analyse ce CV d'un étudiant en {filiere} (année {annee}) {poste_context} :\n\n"
        f"{cv_text[:4000]}\n\n"
        "Fournis une analyse structurée avec :\n"
        "1. **Points forts** (3-5 éléments)\n"
        "2. **Points à améliorer** (3-5 éléments)\n"
        "3. **Compétences manquantes** pour le marché marocain\n"
        "4. **Score global** (sur 10) avec justification\n"
        "5. **Recommandations prioritaires** (3 actions concrètes)\n\n"
        "Sois précis, actionnable et adapté au contexte ENIAD Berkane."
    )
    try:
        from backend.agents.orchestrator import get_llm
        from langchain_core.messages import SystemMessage as _SMsg, HumanMessage as _HMsg
        llm = get_llm()
        resp = llm.invoke([_SMsg(content=prompt_system), _HMsg(content=prompt_user)])
        return {
            "nom": nom, "filiere": filiere,
            "poste_cible": poste_cible or None,
            "cv_filename": cv_file.filename,
            "analyse": resp.content.strip(),
            "generated_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur analyse CV : {e}")


@app.post("/api/orientation/generate-lm", tags=["Orientation"])
async def generate_lm(
    body: _LmGenerateRequest,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Générer une lettre de motivation personnalisée pour un stage ou emploi."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    nom = user.full_name or user.username or "Étudiant ENIAD"
    filiere = getattr(profile, "major", None) or "Génie Informatique"
    annee = getattr(profile, "year", None) or 3
    niveau_map = {1: "1ère", 2: "2ème", 3: "3ème", 4: "4ème", 5: "5ème"}
    niveau = niveau_map.get(int(annee) if annee else 3, f"{annee}ème")
    type_context = (
        "startup marocaine, ton flexible, innovant et orienté résultats"
        if body.type_lm == "startup"
        else "grande entreprise ou multinationale, ton professionnel, structuré et formel"
    )
    competences_ctx = f"\nCompétences à valoriser : {body.competences}" if body.competences else ""
    projets_ctx = f"\nProjets/expériences : {body.projets}" if body.projets else ""
    prompt_system = (
        "Tu es un expert en rédaction de lettres de motivation pour ingénieurs au Maroc. "
        "Tu génères des lettres professionnelles, personnalisées, en français, adaptées au contexte marocain."
    )
    prompt_user = (
        f"Génère une lettre de motivation complète pour :\n"
        f"- Candidat : {nom} ({niveau} année {filiere}, ENIAD Berkane)\n"
        f"- Poste : {body.poste}\n"
        f"- Entreprise : {body.entreprise}\n"
        f"- Style : {type_context}\n"
        f"{competences_ctx}{projets_ctx}\n\n"
        "Structure : en-tête coordonnées, objet, introduction, 2 paragraphes développement, conclusion, formule de politesse.\n"
        "Génère UNIQUEMENT le texte de la lettre, prêt à copier-coller."
    )
    try:
        from backend.agents.orchestrator import get_llm
        from langchain_core.messages import SystemMessage as _SMsg, HumanMessage as _HMsg
        llm = get_llm()
        resp = llm.invoke([_SMsg(content=prompt_system), _HMsg(content=prompt_user)])
        return {
            "nom": nom, "poste": body.poste, "entreprise": body.entreprise,
            "filiere": filiere, "lettre": resp.content.strip(),
            "generated_at": datetime.utcnow().isoformat(),
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur génération LM : {e}")


_ORIENTATION_STAGES = [
    {"entreprise": "OCP Group", "poste": "Stage PFE — IA & Data Science", "lieu": "Khouribga / Casablanca", "duree": "4–6 mois", "profil": ["IA", "GINF"], "description": "Optimisation des processus industriels par ML et analyse de données massives.", "type": "pfe", "lien": "https://www.ocpgroup.ma/fr/carrieres"},
    {"entreprise": "Maroc Telecom", "poste": "Stage PFE — Cybersécurité & Réseaux", "lieu": "Rabat, Maroc", "duree": "4–6 mois", "profil": ["IRSI"], "description": "Sécurisation des infrastructures télécom, audit de sécurité, SOC.", "type": "pfe", "lien": "https://www.iam.ma/fr/carrieres"},
    {"entreprise": "Capgemini Maroc", "poste": "Stage Full Stack / IA", "lieu": "Casablanca, Maroc", "duree": "2–6 mois", "profil": ["GINF", "IA"], "description": "Développement d'applications web et mobiles pour clients internationaux.", "type": "alternance", "lien": "https://www.capgemini.com/fr-fr/carrieres/"},
    {"entreprise": "INWI", "poste": "Stage IoT & Réseaux 5G", "lieu": "Casablanca, Maroc", "duree": "3–6 mois", "profil": ["ROC", "IRSI"], "description": "Déploiement IoT, optimisation réseaux mobiles, projets 5G.", "type": "pfe", "lien": "https://www.inwi.ma/fr/carrieres"},
    {"entreprise": "UM6P / OCP Innovation", "poste": "Stage Data Engineer & Robotique", "lieu": "Ben Guerir, Maroc", "duree": "3–4 mois", "profil": ["IA", "GINF", "ROC"], "description": "Projets de recherche appliquée en IA, robotique et transformation digitale.", "type": "recherche", "lien": "https://www.um6p.ma/fr"},
    {"entreprise": "CGI Maroc", "poste": "Stage DevOps & Cloud", "lieu": "Casablanca, Maroc", "duree": "3–6 mois", "profil": ["GINF", "IRSI"], "description": "Infrastructure cloud AWS/Azure, CI/CD, automatisation.", "type": "alternance", "lien": "https://www.cgi.com/fr/fr-fr/carrieres"},
    {"entreprise": "Atos Maroc", "poste": "Stage Développement & Cybersécurité", "lieu": "Casablanca, Maroc", "duree": "2–6 mois", "profil": ["GINF", "IRSI", "IA"], "description": "Projets de transformation digitale, sécurité des systèmes d'information.", "type": "pfe", "lien": "https://atos.net/fr/recrutement"},
    {"entreprise": "Leoni Maroc", "poste": "Stage Automatisation Industrielle / IoT", "lieu": "Ain Sebaâ, Casablanca", "duree": "4–6 mois", "profil": ["ROC", "GINF"], "description": "Automatisation de lignes de production, capteurs industriels, SCADA.", "type": "pfe", "lien": "https://www.leoni.com/fr/carriere/"},
    {"entreprise": "SGMB / Bank Al-Maghrib", "poste": "Stage Data Science & Analyse Risques", "lieu": "Rabat / Casablanca", "duree": "3–6 mois", "profil": ["IA", "GINF"], "description": "Modèles prédictifs, scoring crédit, analyse de données financières.", "type": "pfe", "lien": "https://rekrute.com"},
    {"entreprise": "Startups Technopark", "poste": "Stage Développement / IA", "lieu": "Casablanca / Rabat", "duree": "1–3 mois", "profil": ["IA", "GINF", "IRSI", "ROC"], "description": "Environnement startup, polyvalence, projets innovants à fort impact.", "type": "stage", "lien": "https://www.technopark.ma"},
]

_ORIENTATION_PLATFORMS = [
    {"nom": "Rekrute.ma", "description": "Principal portail emploi marocain", "lien": "https://rekrute.com"},
    {"nom": "Stage.ma", "description": "Spécialisé stages au Maroc", "lien": "https://www.stage.ma"},
    {"nom": "LinkedIn Jobs", "description": "Offres stages et emplois internationaux", "lien": "https://www.linkedin.com/jobs/"},
    {"nom": "ANAPEC", "description": "Programme de stage conventionné gouvernement", "lien": "https://www.anapec.org"},
]

_FILIERE_KEYWORDS: dict = {
    "IA":   ["IA", "INTELLIGENCE", "ARTIFICIELLE", "AI"],
    "GINF": ["GINF", "INFORMATIQUE", "LOGICIEL", "SOFTWARE"],
    "IRSI": ["IRSI", "RESEAU", "SECURITE", "NETWORK"],
    "ROC":  ["ROC", "ROBOTIQUE", "IOT", "ROBOT"],
}

@app.get("/api/orientation/stages", tags=["Orientation"])
async def get_stages(
    filiere: Optional[str] = None,
    type_stage: Optional[str] = None,
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db),
):
    """Retourner les opportunités de stage adaptées à la filière de l'étudiant."""
    user = await get_current_user(authorization, db)
    profile = db.query(UserProfile).filter(UserProfile.user_id == user.id).first()
    student_filiere = filiere or getattr(profile, "major", None) or ""

    matched_filiere = None
    if student_filiere:
        fili_upper = student_filiere.upper()
        for key, kws in _FILIERE_KEYWORDS.items():
            if any(kw in fili_upper for kw in kws):
                matched_filiere = key
                break

    filtered = [
        s for s in _ORIENTATION_STAGES
        if not matched_filiere or matched_filiere in s["profil"]
    ]
    if type_stage and type_stage in ("pfe", "stage", "alternance", "recherche"):
        filtered = [s for s in filtered if s.get("type") == type_stage]

    return {
        "filiere": student_filiere or "Toutes filières",
        "stages": filtered,
        "platforms": _ORIENTATION_PLATFORMS,
        "total": len(filtered),
        "generated_at": datetime.utcnow().isoformat(),
    }


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
