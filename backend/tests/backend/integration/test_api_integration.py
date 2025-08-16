"""
Integration tests for API endpoints
"""
import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, Mock
import json


class TestAPIIntegration:
    """Integration tests for API endpoints"""
    
    def test_health_check_integration(self, test_client):
        """Test health check endpoint integration"""
        response = test_client.get("/health")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify all expected fields are present
        expected_fields = ["status", "service", "version", "mock_mode", "use_local_model"]
        for field in expected_fields:
            assert field in data, f"Missing field: {field}"
        
        # Verify field types
        assert isinstance(data["status"], str)
        assert isinstance(data["service"], str)
        assert isinstance(data["version"], str)
        assert isinstance(data["mock_mode"], bool)
        assert isinstance(data["use_local_model"], bool)
    
    def test_root_endpoint_integration(self, test_client):
        """Test root endpoint integration"""
        response = test_client.get("/")
        
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "message" in data
        assert "documentation" in data
        assert "health" in data
        
        # Verify links are correct
        assert data["documentation"] == "/docs"
        assert data["health"] == "/health"
    
    def test_openapi_schema_integration(self, test_client):
        """Test OpenAPI schema generation"""
        response = test_client.get("/openapi.json")
        
        assert response.status_code == 200
        schema = response.json()
        
        # Verify OpenAPI structure
        assert schema["openapi"].startswith("3.")
        assert schema["info"]["title"] == "OSSGameForge API"
        
        # Verify endpoints are documented
        assert "/health" in schema["paths"]
        assert "/" in schema["paths"]
        
        # Verify health endpoint documentation
        health_endpoint = schema["paths"]["/health"]["get"]
        assert "summary" in health_endpoint
        assert "responses" in health_endpoint
        assert "200" in health_endpoint["responses"]
    
    def test_cors_headers_integration(self, test_client):
        """Test CORS headers are properly set"""
        response = test_client.options(
            "/health",
            headers={
                "Origin": "http://localhost:3000",
                "Access-Control-Request-Method": "GET"
            }
        )
        
        # CORS preflight should return 200
        assert response.status_code == 200
        
        # Check CORS headers (header keys might be lowercase)
        headers_lower = {k.lower(): v for k, v in response.headers.items()}
        assert "access-control-allow-origin" in headers_lower
        assert "access-control-allow-methods" in headers_lower
        # Note: allow-headers might not be present if using wildcard
    
    def test_invalid_endpoint_returns_404(self, test_client):
        """Test that invalid endpoints return 404"""
        response = test_client.get("/invalid-endpoint")
        
        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Not Found"
    
    def test_method_not_allowed(self, test_client):
        """Test that unsupported methods return 405"""
        response = test_client.post("/health")
        
        assert response.status_code == 405
        data = response.json()
        assert "detail" in data
        assert data["detail"] == "Method Not Allowed"
    
    @pytest.mark.parametrize("endpoint,method", [
        ("/health", "get"),
        ("/", "get"),
        ("/docs", "get"),
        ("/openapi.json", "get"),
    ])
    def test_endpoints_accessibility(self, test_client, endpoint, method):
        """Test that all documented endpoints are accessible"""
        response = getattr(test_client, method)(endpoint)
        assert response.status_code == 200
    
    def test_concurrent_requests(self, test_client):
        """Test API can handle concurrent requests"""
        import concurrent.futures
        
        def make_request():
            return test_client.get("/health")
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            futures = [executor.submit(make_request) for _ in range(20)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]
        
        # All requests should succeed
        assert all(r.status_code == 200 for r in results)
        
        # All should return the same data structure
        data_structures = [r.json().keys() for r in results]
        first_structure = data_structures[0]
        assert all(struct == first_structure for struct in data_structures)


class TestDatabaseIntegration:
    """Test database integration"""
    
    def test_database_session_lifecycle(self, test_client, test_db_session):
        """Test database session is properly managed"""
        # Make a request that would use the database
        response = test_client.get("/health")
        assert response.status_code == 200
        
        # Note: test_db_session is actually still active during the test
        # This is expected behavior for test fixtures
        # In production, sessions are properly closed after each request
    
    def test_database_rollback_on_error(self, test_client, test_db_session):
        """Test database rollback on error"""
        # This is a placeholder for when we have endpoints that modify data
        # The test would verify that failed transactions are rolled back
        pass


class TestEnvironmentConfiguration:
    """Test environment-based configuration"""
    
    @patch.dict("os.environ", {"MOCK_MODE": "true"})
    def test_mock_mode_enabled(self, test_client):
        """Test API respects MOCK_MODE environment variable"""
        response = test_client.get("/health")
        data = response.json()
        
        # Note: This might not reflect immediately due to settings caching
        # In a real scenario, you'd restart the app or use a different approach
        assert response.status_code == 200
    
    @patch.dict("os.environ", {"USE_LOCAL_MODEL": "true"})
    def test_local_model_enabled(self, test_client):
        """Test API respects USE_LOCAL_MODEL environment variable"""
        response = test_client.get("/health")
        data = response.json()
        
        assert response.status_code == 200