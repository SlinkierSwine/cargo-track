import pytest
from unittest.mock import AsyncMock, MagicMock
from uuid import UUID, uuid4
from entities.user import User, UserCreate, UserUpdate, UserRole
from repositories.user_repository import UserRepository


@pytest.fixture
def f_user_repository():
    # This will be implemented later - for now it's just an abstract class
    # Tests should fail until we implement a concrete repository
    return None


@pytest.fixture
def f_valid_user_data():
    return UserCreate(
        email="test@example.com",
        username="testuser",
        password="TestPass123",
        role=UserRole.CLIENT,
        first_name="Test",
        last_name="User"
    )


async def test_create_user_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    
    assert created_user.email == f_valid_user_data.email
    assert created_user.username == f_valid_user_data.username
    assert created_user.role == f_valid_user_data.role
    assert created_user.first_name == f_valid_user_data.first_name
    assert created_user.last_name == f_valid_user_data.last_name
    assert created_user.hashed_password == "hashed_" + f_valid_user_data.password


async def test_get_by_id_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    
    found_user = await f_user_repository.get_by_id(created_user.id)
    
    assert found_user is not None
    assert found_user.id == created_user.id
    assert found_user.email == created_user.email


async def test_get_by_id_not_found(f_user_repository):
    non_existent_id = uuid4()
    
    found_user = await f_user_repository.get_by_id(non_existent_id)
    
    assert found_user is None


async def test_get_by_email_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    
    found_user = await f_user_repository.get_by_email(f_valid_user_data.email)
    
    assert found_user is not None
    assert found_user.email == f_valid_user_data.email


async def test_get_by_email_not_found(f_user_repository):
    found_user = await f_user_repository.get_by_email("nonexistent@example.com")
    
    assert found_user is None


async def test_get_by_username_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    
    found_user = await f_user_repository.get_by_username(f_valid_user_data.username)
    
    assert found_user is not None
    assert found_user.username == f_valid_user_data.username


async def test_get_by_username_not_found(f_user_repository):
    found_user = await f_user_repository.get_by_username("nonexistent")
    
    assert found_user is None


async def test_update_user_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    update_data = UserUpdate(first_name="Updated", last_name="Name")
    
    updated_user = await f_user_repository.update(created_user.id, update_data)
    
    assert updated_user is not None
    assert updated_user.first_name == "Updated"
    assert updated_user.last_name == "Name"
    assert updated_user.email == f_valid_user_data.email  # unchanged


async def test_update_user_not_found(f_user_repository):
    non_existent_id = uuid4()
    update_data = UserUpdate(first_name="Updated")
    
    updated_user = await f_user_repository.update(non_existent_id, update_data)
    
    assert updated_user is None


async def test_delete_user_success(f_user_repository, f_valid_user_data):
    created_user = await f_user_repository.create(f_valid_user_data)
    
    result = await f_user_repository.delete(created_user.id)
    
    assert result is True
    found_user = await f_user_repository.get_by_id(created_user.id)
    assert found_user is None


async def test_delete_user_not_found(f_user_repository):
    non_existent_id = uuid4()
    
    result = await f_user_repository.delete(non_existent_id)
    
    assert result is False


async def test_list_users(f_user_repository, f_valid_user_data):
    user1 = await f_user_repository.create(f_valid_user_data)
    user2_data = UserCreate(
        email="test2@example.com",
        username="testuser2",
        password="TestPass123",
        role=UserRole.DRIVER
    )
    user2 = await f_user_repository.create(user2_data)
    
    users = await f_user_repository.list_users()
    
    assert len(users) == 2
    assert any(u.id == user1.id for u in users)
    assert any(u.id == user2.id for u in users) 