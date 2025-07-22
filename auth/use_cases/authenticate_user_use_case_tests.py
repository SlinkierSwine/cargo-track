import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from entities.user import User, UserRole
from entities.token import Token
from use_cases.authenticate_user_use_case import AuthenticateUserUseCase


@pytest.fixture
def m_user_repository():
    return AsyncMock()


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


@patch('use_cases.authenticate_user_use_case.verify_password')
@patch('use_cases.authenticate_user_use_case.create_access_token')
async def test_authenticate_user_success(m_create_token, m_verify_password, 
                                       f_authenticate_use_case, m_user_repository, f_mock_user):
    email = "test@example.com"
    password = "TestPass123"
    expected_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    
    m_user_repository.get_by_email.return_value = f_mock_user
    m_verify_password.return_value = True
    m_create_token.return_value = expected_token
    
    result = await f_authenticate_use_case.execute(email, password)
    
    assert isinstance(result, Token)
    assert result.access_token == expected_token
    assert result.token_type == "bearer"
    m_user_repository.get_by_email.assert_called_once_with(email)
    m_verify_password.assert_called_once_with(password, f_mock_user.hashed_password)
    m_create_token.assert_called_once_with(data={
        "sub": str(f_mock_user.id), 
        "username": f_mock_user.username, 
        "role": f_mock_user.role.value
    })


async def test_authenticate_user_not_found(f_authenticate_use_case, m_user_repository):
    email = "nonexistent@example.com"
    password = "TestPass123"
    
    m_user_repository.get_by_email.return_value = None
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        await f_authenticate_use_case.execute(email, password)
    
    m_user_repository.get_by_email.assert_called_once_with(email)


@patch('use_cases.authenticate_user_use_case.verify_password')
async def test_authenticate_user_invalid_password(m_verify_password, 
                                                f_authenticate_use_case, m_user_repository, f_mock_user):
    email = "test@example.com"
    password = "WrongPassword"
    
    m_user_repository.get_by_email.return_value = f_mock_user
    m_verify_password.return_value = False
    
    with pytest.raises(ValueError, match="Invalid credentials"):
        await f_authenticate_use_case.execute(email, password)
    
    m_user_repository.get_by_email.assert_called_once_with(email)
    m_verify_password.assert_called_once_with(password, f_mock_user.hashed_password)


async def test_authenticate_user_inactive_account(f_authenticate_use_case, m_user_repository, f_mock_user):
    email = "test@example.com"
    password = "TestPass123"
    
    f_mock_user.is_active = False
    m_user_repository.get_by_email.return_value = f_mock_user
    
    with pytest.raises(ValueError, match="Account is deactivated"):
        await f_authenticate_use_case.execute(email, password)
    
    m_user_repository.get_by_email.assert_called_once_with(email) 