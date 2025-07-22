import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from entities.user import UserRole
from main import app


@pytest.fixture
def f_test_client():
    return TestClient(app)


@pytest.fixture
def f_mock_user():
    user = MagicMock()
    user.id = "123e4567-e89b-12d3-a456-426614174000"
    user.email = "test@example.com"
    user.username = "testuser"
    user.role = UserRole.CLIENT
    user.is_active = True
    user.first_name = "Test"
    user.last_name = "User"
    return user


def test_get_user_not_found(f_test_client):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    
    response = f_test_client.get(f"/users/{user_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "User not found" in data["detail"]


def test_get_users_empty(f_test_client):
    response = f_test_client.get("/users")
    
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)


def test_update_user_not_found(f_test_client):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    update_data = {"email": "updated@example.com"}
    
    response = f_test_client.put(f"/users/{user_id}", json=update_data)
    
    assert response.status_code == 404
    data = response.json()
    assert "User not found" in data["detail"]


def test_delete_user_not_found(f_test_client):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    
    response = f_test_client.delete(f"/users/{user_id}")
    
    assert response.status_code == 404
    data = response.json()
    assert "User not found" in data["detail"]


def test_update_user_invalid_data(f_test_client):
    user_id = "123e4567-e89b-12d3-a456-426614174000"
    invalid_data = {"email": "invalid-email"}
    
    response = f_test_client.put(f"/users/{user_id}", json=invalid_data)
    
    assert response.status_code == 422


def test_get_current_user_not_implemented(f_test_client):
    response = f_test_client.get("/users/me")
    
    assert response.status_code == 501
    data = response.json()
    assert "Not implemented yet" in data["detail"] 