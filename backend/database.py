from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from backend.config import get_settings

settings = get_settings()

# Create database engine
engine = create_engine(
    settings.DATABASE_URL,
    echo=settings.DEBUG,
    pool_pre_ping=True,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {}
)

# Create session factory
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

def get_db() -> Session:
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def init_db():
    """Initialize database tables and run lightweight column migrations."""
    from backend.models import Base
    Base.metadata.create_all(bind=engine)
    _migrate_complaints()


def _migrate_complaints():
    """Add new columns to complaints if they don't exist yet (SQLite safe)."""
    new_cols = [
        ("titre",                "TEXT"),
        ("ai_categorie",         "TEXT"),
        ("ai_priorite",          "INTEGER"),
        ("ai_resume",            "TEXT"),
        ("ai_reponse_suggeree",  "TEXT"),
        ("admin_id",             "INTEGER"),
        ("admin_reponse",        "TEXT"),
        ("updated_at",           "DATETIME"),
        ("is_read_by_student",   "INTEGER DEFAULT 1"),
    ]
    with engine.connect() as conn:
        import sqlalchemy as sa
        try:
            existing = {row[1] for row in conn.execute(sa.text("PRAGMA table_info(complaints)"))}
        except Exception:
            return  # table doesn't exist yet — create_all will handle it
        for col_name, col_type in new_cols:
            if col_name not in existing:
                try:
                    conn.execute(sa.text(f"ALTER TABLE complaints ADD COLUMN {col_name} {col_type}"))
                    conn.commit()
                except Exception:
                    pass  # already added by a parallel process or unsupported

def close_db():
    """Close database connections"""
    engine.dispose()
