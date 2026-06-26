from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List, Any

# Auth Schemas
class UserRegister(BaseModel):
    email: str
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_card_id: Optional[str] = None
    field_of_study: Optional[str] = None
    academic_year: Optional[int] = None

class UserLogin(BaseModel):
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    full_name: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    is_active: bool
    is_admin: bool = False
    created_at: datetime

    class Config:
        from_attributes = True

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str
    expires_in: int
    user: UserResponse

# User Profile Schemas
class UserProfileUpdate(BaseModel):
    bio: Optional[str] = None
    avatar_url: Optional[str] = None
    phone: Optional[str] = None
    university: Optional[str] = None
    major: Optional[str] = None
    year: Optional[int] = None
    language: Optional[str] = None
    preferences: Optional[dict] = {}
    student_card_id: Optional[str] = None
    cne: Optional[str] = None
    cin: Optional[str] = None
    date_naissance: Optional[str] = None  # DD/MM/YYYY

class UserProfileResponse(BaseModel):
    id: int
    user_id: int
    bio: Optional[str]
    avatar_url: Optional[str]
    university: Optional[str]
    major: Optional[str]
    year: Optional[int]
    student_card_id: Optional[str] = None
    cne: Optional[str] = None
    cin: Optional[str] = None
    date_naissance: Optional[str] = None
    language: str
    timezone: str
    created_at: datetime

    class Config:
        from_attributes = True

# Message Schemas
class MessageCreate(BaseModel):
    content: str
    message_type: str = "text"
    extra_data: Optional[dict] = {}

class MessageResponse(BaseModel):
    id: int
    user_id: int
    content: str
    sender: str
    message_type: str
    extra_data: dict
    created_at: datetime
    
    class Config:
        from_attributes = True

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    semestre: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    agent: str
    agent_name: Optional[str] = ""
    extra_data: Optional[dict] = {}

# Exam Schemas
class QuestionCreate(BaseModel):
    text: str
    type: str  # multiple_choice, short_answer, essay
    options: Optional[List[str]] = None
    correct_answer: Optional[str] = None
    points: int = 1

class ExamCreate(BaseModel):
    title: str
    subject: str
    questions: List[QuestionCreate]
    total_points: int

class ExamResponse(BaseModel):
    id: int
    user_id: int
    title: str
    subject: str
    score: Optional[int]
    total_points: int
    status: str
    created_at: datetime
    completed_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ExamAnswerSubmit(BaseModel):
    exam_id: int
    answers: List[Any]

# Event Schemas
class EventCreate(BaseModel):
    title: str
    description: Optional[str] = None
    event_type: str
    start_date: datetime
    end_date: Optional[datetime] = None
    location: Optional[str] = None

class EventResponse(BaseModel):
    id: int
    title: str
    description: Optional[str]
    event_type: str
    start_date: datetime
    end_date: Optional[datetime]
    location: Optional[str]
    is_public: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Plan Schemas
class PlanCreate(BaseModel):
    title: str
    description: Optional[str] = None
    category: str
    due_date: datetime
    priority: int = 1

class PlanUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[str] = None
    priority: Optional[int] = None

class PlanResponse(BaseModel):
    id: int
    user_id: int
    title: str
    description: Optional[str]
    category: str
    due_date: datetime
    priority: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

# Memory Schemas
class MemoryCreate(BaseModel):
    category: str
    content: str
    importance: int = 1
    expires_at: Optional[datetime] = None

class MemoryResponse(BaseModel):
    id: int
    user_id: int
    category: str
    content: str
    importance: int
    created_at: datetime
    
    class Config:
        from_attributes = True

# Document Schemas
class DocumentCreate(BaseModel):
    title: str
    content: str
    document_type: str

class DocumentResponse(BaseModel):
    id: int
    title: str
    document_type: str
    file_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
