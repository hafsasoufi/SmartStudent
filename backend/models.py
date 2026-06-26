from sqlalchemy import Column, Integer, Float, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum
import uuid as _uuid

Base = declarative_base()

class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    profile = relationship("UserProfile", uselist=False, back_populates="user")
    messages = relationship("Message", back_populates="user")
    memories = relationship("Memory", back_populates="user")
    exams = relationship("Exam", back_populates="user")
    admin_requests = relationship("AdminRequest", back_populates="user")
    complaints = relationship("Complaint", back_populates="user", foreign_keys="Complaint.user_id")

class UserProfile(Base):
    """Extended user profile information"""
    __tablename__ = "user_profiles"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True)
    bio = Column(Text, nullable=True)
    avatar_url = Column(String, nullable=True)
    phone = Column(String, nullable=True)
    university = Column(String, nullable=True)
    major = Column(String, nullable=True)
    year = Column(Integer, nullable=True)
    student_card_id = Column(String, nullable=True, index=True)
    # Academic identity fields for official documents
    cne = Column(String, nullable=True)            # Code National Étudiant
    cin = Column(String, nullable=True)            # Carte d'Identité Nationale
    date_naissance = Column(String, nullable=True) # DD/MM/YYYY
    language = Column(String, default="en")
    timezone = Column(String, default="UTC")
    preferences = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="profile")

class Message(Base):
    """Chat messages between user and orchestrator"""
    __tablename__ = "messages"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    content = Column(Text)
    sender = Column(String)  # "user" or "assistant"
    message_type = Column(String, default="text")  # text, image, document
    extra_data = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.utcnow)
    
    # Relationships
    user = relationship("User", back_populates="messages")

class Memory(Base):
    """User memory/context for agents"""
    __tablename__ = "memories"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    category = Column(String)  # academic, personal, preferences
    content = Column(Text)
    importance = Column(Integer, default=1)  # 1-10 importance score
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    expires_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="memories")

class Document(Base):
    """Documents for RAG system"""
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    content = Column(Text)
    document_type = Column(String)  # syllabus, announcement, guide, etc
    file_url = Column(String, nullable=True)
    embedding_id = Column(String, nullable=True)  # Pinecone vector ID
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Exam(Base):
    """Exam records and quiz data"""
    __tablename__ = "exams"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    subject = Column(String)
    questions = Column(JSON)  # List of questions
    answers = Column(JSON, nullable=True)  # User's answers
    score = Column(Integer, nullable=True)
    total_points = Column(Integer)
    status = Column(String, default="draft")  # draft, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    started_at = Column(DateTime, nullable=True)
    completed_at = Column(DateTime, nullable=True)
    
    # Relationships
    user = relationship("User", back_populates="exams")

class Event(Base):
    """Campus events and deadlines"""
    __tablename__ = "events"
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String)
    description = Column(Text, nullable=True)
    event_type = Column(String)  # deadline, event, reminder
    start_date = Column(DateTime)
    end_date = Column(DateTime, nullable=True)
    location = Column(String, nullable=True)
    is_public = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Plan(Base):
    """Planning/scheduling data"""
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String)
    description = Column(Text, nullable=True)
    category = Column(String)  # study, project, personal
    due_date = Column(DateTime)
    priority = Column(Integer, default=1)  # 1-5
    status = Column(String, default="pending")  # pending, in_progress, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class AdminRequest(Base):
    """Demandes administratives des etudiants (attestations, releves, conventions...)"""
    __tablename__ = "admin_requests"

    id = Column(String(36), primary_key=True, default=lambda: str(_uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    request_type = Column(String(60), nullable=False)
    status = Column(String(20), default="pending")  # pending|in_progress|validated|refused
    description = Column(Text, nullable=True)
    doc_id = Column(String(100), nullable=True)   # reference au PDF genere
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="admin_requests")


class ExamSchedule(Base):
    """Planning des examens officiels par matière"""
    __tablename__ = "exam_schedules"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    matiere      = Column(String(150), nullable=False)
    date_examen  = Column(DateTime, nullable=False)
    semestre     = Column(String(20), nullable=True)   # S1, S2, S3...
    salle        = Column(String(50), nullable=True)
    coefficient  = Column(Float, default=1.0)
    notes        = Column(Text, nullable=True)
    created_at   = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")


class CourseDocument(Base):
    """Contenu textuel d'un cours importé (PDF ou copie-colle)"""
    __tablename__ = "course_documents"

    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"), nullable=False)
    matiere      = Column(String(150), nullable=False)
    titre        = Column(String(255), nullable=True)
    contenu      = Column(Text, nullable=False)       # texte brut extrait
    resume       = Column(Text, nullable=True)        # résumé IA
    notions_cles = Column(JSON, nullable=True)        # liste de notions importantes
    created_at   = Column(DateTime, default=datetime.utcnow)
    updated_at   = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User")


class Complaint(Base):
    """Tickets de reclamation des etudiants"""
    __tablename__ = "complaints"

    id = Column(String(25), primary_key=True)  # COMP-2026-00001
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    titre = Column(String(200), nullable=True)
    category = Column(String(50), nullable=False)  # pedagogique|administratif|financier|infrastructure|autre
    description = Column(Text, nullable=False)
    status = Column(String(20), default="open")  # open|in_progress|resolved|closed
    # AI analysis fields
    ai_categorie = Column(String(50), nullable=True)
    ai_priorite = Column(Integer, nullable=True)  # 1=haute, 2=moyenne, 3=basse
    ai_resume = Column(Text, nullable=True)
    ai_reponse_suggeree = Column(Text, nullable=True)
    # Admin response fields
    admin_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    admin_reponse = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

    is_read_by_student = Column(Boolean, default=True)  # False = student has unread admin reply

    user = relationship("User", back_populates="complaints", foreign_keys=[user_id])
    admin = relationship("User", foreign_keys=[admin_id])


class MoodEntry(Base):
    """Suivi quotidien de l'humeur de l'etudiant"""
    __tablename__ = "mood_entries"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    rating = Column(Integer, nullable=False)  # 1-5
    note = Column(String(500), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User")
