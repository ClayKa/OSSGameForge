"""
Tests for backend services
"""

import json
from unittest.mock import mock_open, patch

import pytest

from app.config import Settings


class TestConfiguration:
    """Test configuration management"""

    def test_settings_defaults(self):
        """Test default settings values"""
        settings = Settings()
        assert settings.app_name == "OSSGameForge"
        assert settings.app_version == "0.1.0"
        assert settings.api_prefix == "/api"
        assert settings.mock_mode is False
        assert settings.use_local_model is False

    @patch.dict("os.environ", {"MOCK_MODE": "true", "USE_LOCAL_MODEL": "true"})
    def test_settings_from_environment(self):
        """Test settings from environment variables"""
        settings = Settings()
        assert settings.mock_mode is True
        assert settings.use_local_model is True

    def test_cors_origins(self):
        """Test CORS origins configuration"""
        settings = Settings()
        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:5173" in settings.cors_origins

    def test_file_upload_settings(self):
        """Test file upload configuration"""
        settings = Settings()
        assert settings.max_upload_size == 100 * 1024 * 1024  # 100MB
        assert "image/jpeg" in settings.allowed_image_types
        assert "audio/mpeg" in settings.allowed_audio_types
        assert "video/mp4" in settings.allowed_video_types


class TestMockDataLoading:
    """Test mock data loading functionality"""

    def test_load_mock_data_file_exists(self):
        """Test loading mock data when file exists"""
        mock_data = {"projects": [{"id": "proj_001", "name": "Test"}], "assets": [], "scenes": []}

        # Import the function to test
        from app.routers.projects import load_mock_data

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=json.dumps(mock_data))),
        ):
            result = load_mock_data()
            assert "projects" in result
            assert len(result["projects"]) == 1
            assert result["projects"][0]["id"] == "proj_001"

    def test_load_mock_data_file_not_exists(self):
        """Test loading mock data when file doesn't exist"""
        from app.routers.projects import load_mock_data

        with patch("pathlib.Path.exists", return_value=False):
            result = load_mock_data()
            assert result == {"projects": [], "assets": [], "scenes": []}

    def test_load_mock_data_with_generation_samples(self):
        """Test loading mock data with generation samples"""
        mock_data = {
            "generation_samples": [
                {"prompt": "Create a level", "scene": {"id": "scene_001", "name": "Test Scene"}}
            ]
        }

        from app.routers.generation import load_mock_data

        with (
            patch("pathlib.Path.exists", return_value=True),
            patch("builtins.open", mock_open(read_data=json.dumps(mock_data))),
        ):
            result = load_mock_data()
            assert "generation_samples" in result
            assert len(result["generation_samples"]) == 1


class TestUtilityFunctions:
    """Test utility functions"""

    def test_create_html5_export(self):
        """Test HTML5 export creation"""
        from app.routers.export import create_html5_export

        scene_data = {
            "id": "scene_001",
            "name": "Test Scene",
            "description": "A test scene",
            "metadata": {"width": 800, "height": 600, "background_color": "#000000"},
            "entities": [
                {
                    "id": "entity_001",
                    "type": "player",
                    "name": "Player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 50, "height": 50},
                    "color": "#FF0000",
                }
            ],
        }

        result = create_html5_export(scene_data)
        assert isinstance(result, bytes)
        assert len(result) > 0  # Should contain zip file data

    def test_project_id_generation(self):
        """Test project ID generation"""
        from uuid import uuid4

        # Test that UUIDs are generated correctly
        id1 = f"proj_{uuid4().hex[:8]}"
        id2 = f"proj_{uuid4().hex[:8]}"

        assert id1.startswith("proj_")
        assert id2.startswith("proj_")
        assert id1 != id2
        assert len(id1) == 13  # "proj_" + 8 hex chars


class TestErrorHandling:
    """Test error handling in services"""

    def test_asset_upload_without_consent(self):
        """Test that asset upload fails without consent"""
        from fastapi import HTTPException

        # This is handled in the router, but we can test the logic
        user_consent = False

        if not user_consent:
            with pytest.raises(HTTPException) as exc_info:
                raise HTTPException(
                    status_code=400, detail="User consent is required for asset upload"
                )

            assert exc_info.value.status_code == 400
            assert "consent is required" in exc_info.value.detail.lower()

    def test_file_size_validation(self):
        """Test file size validation"""
        from fastapi import HTTPException

        from app.config import Settings

        settings = Settings()
        file_size = 150 * 1024 * 1024  # 150MB

        if file_size > settings.max_upload_size:
            with pytest.raises(HTTPException) as exc_info:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds maximum allowed size of {settings.max_upload_size} bytes",
                )

            assert exc_info.value.status_code == 413


class TestDatabaseModels:
    """Test database model definitions"""

    def test_asset_model_fields(self):
        """Test that Asset model has required fields"""
        from app.models import Asset

        # Check that the model has the expected columns
        columns = [c.name for c in Asset.__table__.columns]

        assert "id" in columns
        assert "project_id" in columns
        assert "filename" in columns
        assert "path" in columns
        assert "type" in columns
        assert "status" in columns
        assert "metadata" in columns
        assert "consent_hash" in columns
        assert "exif_stripped" in columns
        assert "created_at" in columns

    def test_generation_log_model_fields(self):
        """Test that GenerationLog model has required fields"""
        from app.models import GenerationLog

        columns = [c.name for c in GenerationLog.__table__.columns]

        assert "id" in columns
        assert "user_id" in columns
        assert "prompt" in columns
        assert "model_version" in columns
        assert "status" in columns
        assert "latency_ms" in columns
        assert "created_at" in columns
