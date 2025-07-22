import pytest
from unittest.mock import MagicMock
from entities.user import UserCreate, UserRole, User
from use_cases.register_user_use_case import RegisterUserUseCase, RegisterUserRequest


@pytest.fixture
def m_user_repository():
    return MagicMock()


@pytest.fixture
def f_register_use_case(m_user_repository):
    return RegisterUserUseCase(m_user_repository)


@pytest.fixture
def f_valid_user_request():
    return RegisterUserRequest(
        email="test@example.com",
        username="testuser",
        password="TestPass123",
        role=UserRole.CLIENT,
        first_name="Test",
        last_name="User"
    )


def test_register_user_success(f_register_use_case, m_user_repository, f_valid_user_request):
    # Mock repository responses
    m_user_repository.get_by_email.return_value = None
    m_user_repository.get_by_username.return_value = None
    
    mock_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email=f_valid_user_request.email,
        username=f_valid_user_request.username,
        hashed_password="hashed_password",
        role=f_valid_user_request.role,
        is_active=True,
        first_name=f_valid_user_request.first_name,
        last_name=f_valid_user_request.last_name
    )
    m_user_repository.create.return_value = mock_user
    
    # Execute use case
    result = f_register_use_case.execute(f_valid_user_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_request.email)
    m_user_repository.get_by_username.assert_called_once_with(f_valid_user_request.username)
    m_user_repository.create.assert_called_once()
    
    # Verify result
    assert result.id == str(mock_user.id)
    assert result.email == mock_user.email
    assert result.username == mock_user.username
    assert result.role == mock_user.role
    assert result.is_active == mock_user.is_active
    assert result.first_name == mock_user.first_name
    assert result.last_name == mock_user.last_name


def test_register_user_email_already_exists(f_register_use_case, m_user_repository, f_valid_user_request):
    # Mock repository to return existing user
    existing_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email=f_valid_user_request.email,
        username="existinguser",
        hashed_password="hashed_password",
        role=UserRole.CLIENT,
        is_active=True
    )
    m_user_repository.get_by_email.return_value = existing_user
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="User with this email already exists"):
        f_register_use_case.execute(f_valid_user_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_request.email)
    m_user_repository.get_by_username.assert_not_called()
    m_user_repository.create.assert_not_called()


def test_register_user_username_already_exists(f_register_use_case, m_user_repository, f_valid_user_request):
    # Mock repository responses
    m_user_repository.get_by_email.return_value = None
    existing_user = User(
        id="123e4567-e89b-12d3-a456-426614174000",
        email="existing@example.com",
        username=f_valid_user_request.username,
        hashed_password="hashed_password",
        role=UserRole.CLIENT,
        is_active=True
    )
    m_user_repository.get_by_username.return_value = existing_user
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="User with this username already exists"):
        f_register_use_case.execute(f_valid_user_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_valid_user_request.email)
    m_user_repository.get_by_username.assert_called_once_with(f_valid_user_request.username)
    m_user_repository.create.assert_not_called() 