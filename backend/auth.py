from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from backend.config import get_settings

settings = get_settings()

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class TokenData(BaseModel):
    """JWT token payload — enriched with full student context"""
    user_id: int
    username: str
    email: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    student_card_id: Optional[str] = None
    field_of_study: Optional[str] = None
    academic_year: Optional[int] = None


class Token(BaseModel):
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"
    expires_in: int


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(
    user_id: int,
    username: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    student_card_id: Optional[str] = None,
    field_of_study: Optional[str] = None,
    academic_year: Optional[int] = None,
    expires_delta: Optional[timedelta] = None,
) -> str:
    if expires_delta is None:
        expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = datetime.utcnow() + expires_delta
    to_encode = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "student_card_id": student_card_id,
        "field_of_study": field_of_study,
        "academic_year": academic_year,
        "exp": expire,
        "type": "access",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def create_refresh_token(
    user_id: int,
    username: str,
    email: str,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    student_card_id: Optional[str] = None,
    field_of_study: Optional[str] = None,
    academic_year: Optional[int] = None,
) -> str:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "user_id": user_id,
        "username": username,
        "email": email,
        "first_name": first_name,
        "last_name": last_name,
        "student_card_id": student_card_id,
        "field_of_study": field_of_study,
        "academic_year": academic_year,
        "exp": expire,
        "type": "refresh",
    }
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


def verify_token(token: str) -> Optional[TokenData]:
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id: int = payload.get("user_id")
        username: str = payload.get("username")
        email: str = payload.get("email")
        if user_id is None or username is None or email is None:
            return None
        return TokenData(
            user_id=user_id,
            username=username,
            email=email,
            first_name=payload.get("first_name"),
            last_name=payload.get("last_name"),
            student_card_id=payload.get("student_card_id"),
            field_of_study=payload.get("field_of_study"),
            academic_year=payload.get("academic_year"),
        )
    except JWTError:
        return None
