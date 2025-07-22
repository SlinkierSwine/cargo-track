from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from config import get_settings

settings = get_settings()

engine = create_engine(
    settings.database_url,
    echo=settings.debug
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    from entities.database_models import Base
    Base.metadata.create_all(bind=engine) 