import pytest
from unittest.mock import AsyncMock, MagicMock
from entities.user import UserCreate, UserRole, User
from use_cases.register_user_use_case import RegisterUserUseCase


@pytest.fixture
def m_user_repository():
    return AsyncMock()


@pytest.fixture
def f_register_use_case(m_user_repository):
    return RegisterUserUseCase(m_user_repository)


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


async def test_register_user_success(f_register_use_case, m_user_repository, f_valid_user_data):
    m_user_repository.get_by_email.return_value = None
    m_user_repository.get_by_username.return_value = None
    
    created_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email=f_valid_user_data.email,
        username=f_valid_user_data.username,
        hashed_password="hashed_password",
        role=f_valid_user_data.role,
        is_active=True,
        first_name=f_valid_user_data.first_name,
        last_name=f_valid_user_data.last_name
    )
    
    m_user_repository.create.return_value = created_user
    
    result = await f_register_use_case.execute(f_valid_user_data)
    
    assert result.email == f_valid_user_data.email
    assert result.username == f_valid_user_data.username
    assert result.role == f_valid_user_data.role
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_data.email)
    m_user_repository.get_by_username.assert_called_once_with(f_valid_user_data.username)
    m_user_repository.create.assert_called_once_with(f_valid_user_data)


async def test_register_user_email_already_exists(f_register_use_case, m_user_repository, f_valid_user_data):
    existing_user = MagicMock()
    m_user_repository.get_by_email.return_value = existing_user
    
    with pytest.raises(ValueError, match="User with this email already exists"):
        await f_register_use_case.execute(f_valid_user_data)
    
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_data.email)
    m_user_repository.get_by_username.assert_not_called()
    m_user_repository.create.assert_not_called()


async def test_register_user_username_already_taken(f_register_use_case, m_user_repository, f_valid_user_data):
    m_user_repository.get_by_email.return_value = None
    existing_user = MagicMock()
    m_user_repository.get_by_username.return_value = existing_user
    
    with pytest.raises(ValueError, match="Username already taken"):
        await f_register_use_case.execute(f_valid_user_data)
    
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_data.email)
    m_user_repository.get_by_username.assert_called_once_with(f_valid_user_data.username)
    m_user_repository.create.assert_not_called() 