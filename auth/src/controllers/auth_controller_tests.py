import pytest
from unittest.mock import MagicMock, patch
from fastapi.testclient import TestClient
from entities.user import UserRole
from main import app


@pytest.fixture
def f_test_client():
    return TestClient(app)


@pytest.fixture
def f_register_request_data():
    return {
        "email": "test@example.com",
        "username": "testuser",
        "password": "TestPass123",
        "role": UserRole.CLIENT.value,
        "first_name": "Test",
        "last_name": "User"
    }


@pytest.fixture
def f_authenticate_request_data():
    return {
        "email": "test@example.com",
        "password": "TestPass123"
    }


def test_register_user_validation_error(f_test_client, f_register_request_data):
    # Test with invalid email
    invalid_data = f_register_request_data.copy()
    invalid_data["email"] = "invalid-email"
    
    response = f_test_client.post("/auth/register", json=invalid_data)
    
    assert response.status_code == 422


def test_authenticate_user_validation_error(f_test_client, f_authenticate_request_data):
    # Test with missing password
    invalid_data = {"email": "test@example.com"}
    
    response = f_test_client.post("/auth/login", json=invalid_data)
    
    assert response.status_code == 422


def test_register_user_missing_required_fields(f_test_client):
    # Test with missing required fields
    invalid_data = {
        "email": "test@example.com"
        # missing username and password
    }
    
    response = f_test_client.post("/auth/register", json=invalid_data)
    
    assert response.status_code == 422


def test_register_user_invalid_role(f_test_client, f_register_request_data):
    # Test with invalid role
    invalid_data = f_register_request_data.copy()
    invalid_data["role"] = "INVALID_ROLE"
    
    response = f_test_client.post("/auth/register", json=invalid_data)
    
    assert response.status_code == 422 