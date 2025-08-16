"""
Test health check endpoints
"""
from fastapi.testclient import TestClient


def test_health_check(test_client: TestClient):
    """Test the health check endpoint returns expected status"""
    response = test_client.get("/health")
    assert response.status_code == 200

    data = response.json()
    assert data["status"] == "healthy"
    assert data["service"] == "ossgameforge-backend"
    assert "version" in data
    assert "mock_mode" in data
    assert "use_local_model" in data

def test_root_endpoint(test_client: TestClient):
    """Test the root endpoint returns API information"""
    response = test_client.get("/")
    assert response.status_code == 200

    data = response.json()
    assert "message" in data
    assert "OSSGameForge" in data["message"]
    assert data["documentation"] == "/docs"
    assert data["health"] == "/health"

def test_openapi_schema_available(test_client: TestClient):
    """Test that OpenAPI schema is available"""
    response = test_client.get("/openapi.json")
    assert response.status_code == 200

    data = response.json()
    assert "openapi" in data
    assert "info" in data
    assert data["info"]["title"] == "OSSGameForge API"

def test_docs_available(test_client: TestClient):
    """Test that API documentation is available"""
    response = test_client.get("/docs")
    assert response.status_code == 200
    assert "swagger" in response.text.lower() or "redoc" in response.text.lower()
