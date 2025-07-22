import pytest
from sqlalchemy.orm import Session
from sqlalchemy import text
from config.database import SessionLocal
from entities.database_models import Base
from repositories.user_repository import UserRepository


@pytest.fixture
def f_db_session() -> Session:
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture
def f_user_repository(f_db_session: Session) -> UserRepository:
    return UserRepository(f_db_session)


@pytest.fixture(autouse=True)
def f_clean_db(f_db_session: Session) -> None:
    """Clean database before each test"""
    try:
        f_db_session.execute(text("TRUNCATE TABLE users RESTART IDENTITY CASCADE"))
        f_db_session.commit()
    except Exception:
        # If tables don't exist yet, ignore the error
        pass