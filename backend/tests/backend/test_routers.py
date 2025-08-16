"""
Integration tests for API routers
"""

from unittest.mock import patch

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health endpoint returns correct status"""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert data["service"] == "ossgameforge-backend"
        assert "version" in data
        assert "mock_mode" in data
        assert "use_local_model" in data


class TestProjectsRouter:
    """Test projects API endpoints"""

    @patch("backend.app.config.settings.mock_mode", True)
    def test_list_projects_mock_mode(self):
        """Test listing projects in mock mode"""
        with patch("backend.app.routers.projects.load_mock_data") as mock_load:
            mock_load.return_value = {
                "projects": [
                    {
                        "id": "proj_001",
                        "name": "Test Project",
                        "description": "Test description",
                        "owner": "test_user",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "assets_count": 0,
                        "scenes_count": 0,
                    }
                ]
            }

            response = client.get("/api/projects/")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0
            assert data[0]["id"] == "proj_001"

    @patch("backend.app.config.settings.mock_mode", True)
    def test_create_project_mock_mode(self):
        """Test creating a project in mock mode"""
        project_data = {"name": "New Project", "description": "New project description"}

        response = client.post("/api/projects/", json=project_data)
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == project_data["name"]
        assert data["description"] == project_data["description"]
        assert "id" in data
        assert "created_at" in data

    @patch("backend.app.config.settings.mock_mode", True)
    def test_get_project_mock_mode(self):
        """Test getting a single project in mock mode"""
        with patch("backend.app.routers.projects.load_mock_data") as mock_load:
            mock_load.return_value = {
                "projects": [
                    {
                        "id": "proj_001",
                        "name": "Test Project",
                        "description": "Test description",
                        "owner": "test_user",
                        "created_at": "2024-01-01T00:00:00Z",
                        "updated_at": "2024-01-01T00:00:00Z",
                        "assets_count": 0,
                        "scenes_count": 0,
                    }
                ]
            }

            response = client.get("/api/projects/proj_001")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "proj_001"

    @patch("backend.app.config.settings.mock_mode", True)
    def test_get_project_not_found(self):
        """Test getting a non-existent project"""
        with patch("backend.app.routers.projects.load_mock_data") as mock_load:
            mock_load.return_value = {"projects": []}

            response = client.get("/api/projects/nonexistent")
            assert response.status_code == 404


class TestAssetsRouter:
    """Test assets API endpoints"""

    @patch("backend.app.config.settings.mock_mode", True)
    def test_upload_asset_with_consent(self):
        """Test uploading an asset with user consent"""
        # Create a test file
        files = {"file": ("test.txt", b"test content", "text/plain")}
        data = {"user_consent": "true"}

        response = client.post("/api/projects/proj_001/assets", files=files, data=data)
        assert response.status_code == 202
        result = response.json()
        assert "asset_id" in result
        assert result["status"] == "processing"

    @patch("backend.app.config.settings.mock_mode", True)
    def test_upload_asset_without_consent(self):
        """Test uploading an asset without user consent"""
        files = {"file": ("test.txt", b"test content", "text/plain")}
        data = {"user_consent": "false"}

        response = client.post("/api/projects/proj_001/assets", files=files, data=data)
        assert response.status_code == 400
        assert "consent is required" in response.json()["detail"].lower()

    @patch("backend.app.config.settings.mock_mode", True)
    def test_list_project_assets(self):
        """Test listing assets for a project"""
        with patch("backend.app.routers.assets.load_mock_data") as mock_load:
            mock_load.return_value = {
                "assets": [
                    {
                        "id": "asset_001",
                        "project_id": "proj_001",
                        "filename": "test.png",
                        "path": "/assets/test.png",
                        "type": "image",
                        "status": "processed",
                        "metadata": {},
                        "consent_hash": "abc123",
                        "exif_stripped": True,
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ]
            }

            response = client.get("/api/projects/proj_001/assets")
            assert response.status_code == 200
            data = response.json()
            assert isinstance(data, list)
            assert len(data) > 0

    @patch("backend.app.config.settings.mock_mode", True)
    def test_get_asset(self):
        """Test getting a single asset"""
        with patch("backend.app.routers.assets.load_mock_data") as mock_load:
            mock_load.return_value = {
                "assets": [
                    {
                        "id": "asset_001",
                        "project_id": "proj_001",
                        "filename": "test.png",
                        "path": "/assets/test.png",
                        "type": "image",
                        "status": "processed",
                        "metadata": {},
                        "consent_hash": "abc123",
                        "exif_stripped": True,
                        "created_at": "2024-01-01T00:00:00Z",
                    }
                ]
            }

            response = client.get("/api/assets/asset_001")
            assert response.status_code == 200
            data = response.json()
            assert data["id"] == "asset_001"


class TestGenerationRouter:
    """Test generation API endpoints"""

    @patch("backend.app.config.settings.mock_mode", True)
    def test_generate_scene(self):
        """Test generating a scene from prompt"""
        with patch("backend.app.routers.generation.load_mock_data") as mock_load:
            mock_load.return_value = {
                "generation_samples": [
                    {
                        "prompt": "Create a forest level",
                        "scene": {
                            "id": "scene_001",
                            "name": "Forest Level",
                            "description": "A forest level",
                            "version": "1.0.0",
                            "metadata": {
                                "width": 1920,
                                "height": 1080,
                                "background_color": "#228B22",
                            },
                            "entities": [],
                        },
                    }
                ]
            }

            generation_data = {"prompt": "Create a forest level", "project_id": "proj_001"}

            response = client.post("/api/generate", json=generation_data)
            assert response.status_code == 200
            data = response.json()
            assert "scene_id" in data
            assert "scene" in data
            assert "generation_time" in data
            assert data["scene"]["project_id"] == "proj_001"

    @patch("backend.app.config.settings.mock_mode", True)
    def test_generate_scene_with_assets(self):
        """Test generating a scene with specific assets"""
        with patch("backend.app.routers.generation.load_mock_data") as mock_load:
            mock_load.return_value = {
                "generation_samples": [
                    {
                        "prompt": "Create a level",
                        "scene": {
                            "id": "scene_001",
                            "name": "Level",
                            "description": "A level",
                            "version": "1.0.0",
                            "metadata": {
                                "width": 1920,
                                "height": 1080,
                                "background_color": "#87CEEB",
                            },
                            "entities": [],
                        },
                    }
                ]
            }

            generation_data = {
                "prompt": "Create a level",
                "project_id": "proj_001",
                "assets": ["asset_001", "asset_002"],
            }

            response = client.post("/api/generate", json=generation_data)
            assert response.status_code == 200
            data = response.json()
            assert "scene" in data
            # Check that assets were acknowledged in metadata
            if "used_assets" in data["scene"]["metadata"]:
                assert data["scene"]["metadata"]["used_assets"] == generation_data["assets"]


class TestExportRouter:
    """Test export API endpoints"""

    @patch("backend.app.config.settings.mock_mode", True)
    def test_export_html5(self):
        """Test exporting a scene to HTML5"""
        export_data = {"scene_id": "scene_001", "include_assets": True}

        response = client.post("/api/export?engine=html5", json=export_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "application/zip"
        assert "attachment" in response.headers.get("content-disposition", "")

    @patch("backend.app.config.settings.mock_mode", True)
    def test_export_godot(self):
        """Test exporting a scene to Godot format"""
        export_data = {"scene_id": "scene_001", "include_assets": False}

        response = client.post("/api/export?engine=godot", json=export_data)
        assert response.status_code == 200
        assert response.headers["content-type"] == "text/plain"
        assert "attachment" in response.headers.get("content-disposition", "")

    @patch("backend.app.config.settings.mock_mode", True)
    def test_export_unsupported_engine(self):
        """Test exporting with unsupported engine"""
        export_data = {"scene_id": "scene_001", "include_assets": True}

        response = client.post("/api/export?engine=unity", json=export_data)
        assert response.status_code == 400
        assert "not yet supported" in response.json()["detail"].lower()


class TestAPIDocumentation:
    """Test API documentation endpoints"""

    def test_swagger_ui_accessible(self):
        """Test that Swagger UI is accessible"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()

    def test_openapi_schema_accessible(self):
        """Test that OpenAPI schema is accessible"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        assert "/health" in data["paths"]
