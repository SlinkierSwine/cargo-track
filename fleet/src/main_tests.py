import pytest
from fastapi.testclient import TestClient
from .main import app


@pytest.fixture
def f_client():
    return TestClient(app)


def test_root_endpoint(f_client):
    response = f_client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Fleet Service is running"}


def test_health_check(f_client):
    response = f_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "fleet"} 