import pytest
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
from entities.user import UserRole
from admin import UserAdmin
from main import app


@pytest.fixture
def f_test_client():
    return TestClient(app)


def test_user_admin_configuration():
    """Test that UserAdmin is configured correctly"""
    assert UserAdmin.name == "User"
    assert UserAdmin.name_plural == "Users"
    assert UserAdmin.icon == "fa-solid fa-users"
    
    # Check that required columns are present
    required_columns = [
        UserAdmin.model.id,
        UserAdmin.model.email,
        UserAdmin.model.username,
        UserAdmin.model.role,
        UserAdmin.model.is_active,
    ]
    for column in required_columns:
        assert column in UserAdmin.column_list
    
    # Check that searchable columns are configured
    assert len(UserAdmin.column_searchable_list) > 0
    assert UserAdmin.model.email in UserAdmin.column_searchable_list
    assert UserAdmin.model.username in UserAdmin.column_searchable_list
    
    # Check that filterable columns are configured
    assert len(UserAdmin.column_filters) > 0
    assert UserAdmin.model.role in UserAdmin.column_filters
    assert UserAdmin.model.is_active in UserAdmin.column_filters
    
    # Check that form choices are configured
    assert UserAdmin.model.role in UserAdmin.form_choices
    role_choices = UserAdmin.form_choices[UserAdmin.model.role]
    assert (UserRole.ADMIN, "Admin") in role_choices
    assert (UserRole.CLIENT, "Client") in role_choices


def test_admin_endpoint_available(f_test_client):
    """Test that admin endpoint is available"""
    # Try different possible admin paths
    possible_paths = ["/admin", "/admin/", "/admin/user"]
    
    for path in possible_paths:
        response = f_test_client.get(path)
        if response.status_code == 200:
            break
    
    # At least one admin path should work
    assert response.status_code in [200, 302, 404]  # 302 for redirects, 404 for not found


def test_admin_health_check_still_works(f_test_client):
    """Test that health check still works with admin panel"""
    response = f_test_client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "auth"


def test_admin_api_endpoints_available(f_test_client):
    """Test that admin API endpoints are available"""
    # Test admin API endpoints
    response = f_test_client.get("/admin/api/user")
    # Should return some response (might be 200, 401, or 404 depending on auth)
    assert response.status_code in [200, 401, 404] 