from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, JSON, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime
import enum

Base = declarative_base()

class User(Base):
    """User model for authentication and profile"""
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    username = Column(String, unique=True, index=True)
    full_name = Column(String)
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
