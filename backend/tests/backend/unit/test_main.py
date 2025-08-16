"""
Unit tests for main FastAPI application
"""
import os
import sys
from unittest.mock import patch

import pytest
from fastapi.testclient import TestClient

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..', '..', 'backend'))

from backend.app.main import app, lifespan


class TestMainApp:
    """Test main FastAPI application"""

    def test_app_exists(self):
        """Test that FastAPI app is created"""
        assert app is not None
        assert app.title == "OSSGameForge API"
        assert app.description == "AI-powered game creation suite backend"
        assert app.version == "0.1.0"

    def test_cors_middleware_configured(self):
        """Test CORS middleware is properly configured"""
        # Check if CORS middleware is in the middleware stack
        middleware_found = False
        for middleware in app.user_middleware:
            if middleware.cls.__name__ == 'CORSMiddleware':
                middleware_found = True
                # Check CORS settings - access kwargs instead of options
                if hasattr(middleware, 'kwargs'):
                    assert "http://localhost:3000" in middleware.kwargs.get('allow_origins', [])
                    assert "http://localhost:5173" in middleware.kwargs.get('allow_origins', [])
                    assert middleware.kwargs.get('allow_credentials')
                    assert middleware.kwargs.get('allow_methods') == ["*"]
                    assert middleware.kwargs.get('allow_headers') == ["*"]
                break

        assert middleware_found, "CORS middleware not found"

    @pytest.mark.asyncio
    @patch('backend.app.main.logger')
    @patch.dict(os.environ, {"MOCK_MODE": "true", "USE_LOCAL_MODEL": "false"})
    async def test_lifespan_startup(self, mock_logger):
        """Test lifespan context manager startup"""
        async with lifespan(app) as _:
            # Verify startup logs
            mock_logger.info.assert_any_call("Starting OSSGameForge Backend...")
            mock_logger.info.assert_any_call("Mock Mode: true")
            mock_logger.info.assert_any_call("Local Model: false")

    @pytest.mark.asyncio
    @patch('backend.app.main.logger')
    async def test_lifespan_shutdown(self, mock_logger):
        """Test lifespan context manager shutdown"""
        async with lifespan(app) as _:
            pass

        # Verify shutdown log
        mock_logger.info.assert_any_call("Shutting down OSSGameForge Backend...")

    def test_health_endpoint_exists(self):
        """Test health endpoint is registered"""
        routes = [route.path for route in app.routes]
        assert "/health" in routes

    def test_root_endpoint_exists(self):
        """Test root endpoint is registered"""
        routes = [route.path for route in app.routes]
        assert "/" in routes


class TestHealthEndpoint:
    """Test health check endpoint"""

    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)

    @patch.dict(os.environ, {"MOCK_MODE": "true", "USE_LOCAL_MODEL": "false"})
    def test_health_check_response(self):
        """Test health check returns correct response"""
        response = self.client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert data["status"] == "healthy"
        assert data["service"] == "ossgameforge-backend"
        assert data["version"] == "0.1.0"
        assert data["mock_mode"]
        assert not data["use_local_model"]

    @patch.dict(os.environ, {"MOCK_MODE": "false", "USE_LOCAL_MODEL": "true"})
    def test_health_check_different_config(self):
        """Test health check with different configuration"""
        response = self.client.get("/health")

        assert response.status_code == 200
        data = response.json()

        assert not data["mock_mode"]
        assert data["use_local_model"]


class TestRootEndpoint:
    """Test root endpoint"""

    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)

    def test_root_response(self):
        """Test root endpoint returns correct response"""
        response = self.client.get("/")

        assert response.status_code == 200
        data = response.json()

        assert "message" in data
        assert "OSSGameForge API" in data["message"]
        assert data["documentation"] == "/docs"
        assert data["health"] == "/health"

    def test_root_response_structure(self):
        """Test root endpoint response has all required fields"""
        response = self.client.get("/")
        data = response.json()

        required_fields = ["message", "documentation", "health"]
        for field in required_fields:
            assert field in data, f"Missing required field: {field}"


class TestAPIDocumentation:
    """Test API documentation endpoints"""

    def setup_method(self):
        """Set up test client"""
        self.client = TestClient(app)

    def test_openapi_schema_endpoint(self):
        """Test OpenAPI schema is available"""
        response = self.client.get("/openapi.json")

        assert response.status_code == 200
        data = response.json()

        assert "openapi" in data
        assert "info" in data
        assert data["info"]["title"] == "OSSGameForge API"
        assert data["info"]["version"] == "0.1.0"
        assert "paths" in data

    def test_swagger_ui_endpoint(self):
        """Test Swagger UI is available"""
        response = self.client.get("/docs")

        assert response.status_code == 200
        assert "swagger-ui" in response.text.lower()

    def test_redoc_endpoint(self):
        """Test ReDoc is available"""
        response = self.client.get("/redoc")

        assert response.status_code == 200
        assert "redoc" in response.text.lower()
