import pytest
from unittest.mock import MagicMock, patch
from entities.user import User, UserRole
from entities.token import Token
from use_cases.authenticate_user_use_case import AuthenticateUserUseCase, AuthenticateUserRequest


@pytest.fixture
def m_user_repository():
    return MagicMock()


@pytest.fixture
def f_authenticate_use_case(m_user_repository):
    return AuthenticateUserUseCase(m_user_repository)


@pytest.fixture
def f_mock_user():
    user = MagicMock()
    user.id = "123e4567-e89b-12d3-a456-426614174000"
    user.email = "test@example.com"
    user.username = "testuser"
    user.hashed_password = "hashed_password"
    user.role = UserRole.CLIENT
    user.is_active = True
    return user


@pytest.fixture
def f_authenticate_request():
    return AuthenticateUserRequest(
        email="test@example.com",
        password="TestPass123"
    )


def test_authenticate_user_success(f_authenticate_use_case, m_user_repository, f_mock_user, f_authenticate_request):
    # Mock repository and password verification
    m_user_repository.get_by_email.return_value = f_mock_user
    
    with patch('use_cases.authenticate_user_use_case.verify_password', return_value=True):
        with patch('use_cases.authenticate_user_use_case.create_access_token', return_value="test_token"):
            # Execute use case
            result = f_authenticate_use_case.execute(f_authenticate_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_authenticate_request.email)
    
    # Verify result
    assert result.access_token == "test_token"
    assert result.token_type == "bearer"


def test_authenticate_user_not_found(f_authenticate_use_case, m_user_repository, f_authenticate_request):
    # Mock repository to return None
    m_user_repository.get_by_email.return_value = None
    
    # Execute and expect exception
    with pytest.raises(ValueError, match="Invalid email or password"):
        f_authenticate_use_case.execute(f_authenticate_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_authenticate_request.email)


def test_authenticate_user_invalid_password(f_authenticate_use_case, m_user_repository, f_mock_user, f_authenticate_request):
    # Mock repository and password verification
    m_user_repository.get_by_email.return_value = f_mock_user
    
    with patch('use_cases.authenticate_user_use_case.verify_password', return_value=False):
        # Execute and expect exception
        with pytest.raises(ValueError, match="Invalid email or password"):
            f_authenticate_use_case.execute(f_authenticate_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_authenticate_request.email)


def test_authenticate_user_inactive_account(f_authenticate_use_case, m_user_repository, f_authenticate_request):
    # Mock repository to return inactive user
    inactive_user = MagicMock()
    inactive_user.id = "123e4567-e89b-12d3-a456-426614174000"
    inactive_user.email = "test@example.com"
    inactive_user.hashed_password = "hashed_password"
    inactive_user.is_active = False
    
    m_user_repository.get_by_email.return_value = inactive_user
    
    with patch('use_cases.authenticate_user_use_case.verify_password', return_value=True):
        # Execute and expect exception
        with pytest.raises(ValueError, match="User account is disabled"):
            f_authenticate_use_case.execute(f_authenticate_request)
    
    # Verify repository calls
    m_user_repository.get_by_email.assert_called_once_with(f_authenticate_request.email) 