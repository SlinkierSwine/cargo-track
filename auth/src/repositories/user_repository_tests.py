import pytest
from uuid import uuid4

from entities.user import User, UserCreate, UserUpdate, UserRole
from repositories.user_repository import UserRepository


@pytest.fixture
def f_user_create_data():
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="password123",
        role=UserRole.CLIENT,
        first_name="John",
        last_name="Doe"
    )


@pytest.fixture
def f_user_update_data():
    return UserUpdate(
        email="newemail@example.com",
        first_name="Jane"
    )


def test_create_user(f_user_repository: UserRepository, f_user_create_data: UserCreate):
    user = f_user_repository.create(f_user_create_data)
    
    assert user.id is not None
    assert user.email == f_user_create_data.email
    assert user.username == f_user_create_data.username
    assert user.role == f_user_create_data.role
    assert user.is_active is True
    assert user.first_name == f_user_create_data.first_name
    assert user.last_name == f_user_create_data.last_name


def test_get_by_id(f_user_repository: UserRepository, f_user_create_data: UserCreate):
    created_user = f_user_repository.create(f_user_create_data)
    user = f_user_repository.get_by_id(created_user.id)
    
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email


def test_get_by_id_not_found(f_user_repository: UserRepository):
    user = f_user_repository.get_by_id(uuid4())
    assert user is None


def test_get_by_email(f_user_repository: UserRepository, f_user_create_data: UserCreate):
    created_user = f_user_repository.create(f_user_create_data)
    user = f_user_repository.get_by_email(created_user.email)
    
    assert user is not None
    assert user.id == created_user.id
    assert user.email == created_user.email


def test_get_by_email_not_found(f_user_repository: UserRepository):
    user = f_user_repository.get_by_email("nonexistent@example.com")
    assert user is None


def test_get_by_username(f_user_repository: UserRepository, f_user_create_data: UserCreate):
    created_user = f_user_repository.create(f_user_create_data)
    user = f_user_repository.get_by_username(created_user.username)
    
    assert user is not None
    assert user.id == created_user.id
    assert user.username == created_user.username


def test_get_by_username_not_found(f_user_repository: UserRepository):
    user = f_user_repository.get_by_username("nonexistent")
    assert user is None


def test_update_user(f_user_repository: UserRepository, f_user_create_data: UserCreate, f_user_update_data: UserUpdate):
    created_user = f_user_repository.create(f_user_create_data)
    updated_user = f_user_repository.update(created_user.id, f_user_update_data)
    
    assert updated_user is not None
    assert updated_user.id == created_user.id
    assert updated_user.email == f_user_update_data.email
    assert updated_user.first_name == f_user_update_data.first_name
    assert updated_user.username == created_user.username  # unchanged


def test_update_user_not_found(f_user_repository: UserRepository, f_user_update_data: UserUpdate):
    user = f_user_repository.update(uuid4(), f_user_update_data)
    assert user is None


def test_delete_user(f_user_repository: UserRepository, f_user_create_data: UserCreate):
    created_user = f_user_repository.create(f_user_create_data)
    deleted = f_user_repository.delete(created_user.id)
    
    assert deleted is True
    
    # Verify user is deleted
    user = f_user_repository.get_by_id(created_user.id)
    assert user is None


def test_delete_user_not_found(f_user_repository: UserRepository):
    deleted = f_user_repository.delete(uuid4())
    assert deleted is False


def test_list_users(f_user_repository: UserRepository):
    # Create multiple users
    user1_data = UserCreate(
        email="user1@example.com",
        username="user1",
        password="password123",
        role=UserRole.CLIENT
    )
    user2_data = UserCreate(
        email="user2@example.com",
        username="user2",
        password="password123",
        role=UserRole.DRIVER
    )
    
    f_user_repository.create(user1_data)
    f_user_repository.create(user2_data)
    
    users = f_user_repository.list_users()
    assert len(users) >= 2
    
    # Test pagination
    users_limited = f_user_repository.list_users(skip=0, limit=1)
    assert len(users_limited) == 1 