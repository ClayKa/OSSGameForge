"""
Unit tests for configuration module
"""

import os
import sys
from unittest.mock import patch

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "..", "..", "backend"))

from app.config import Settings


class TestSettings:
    """Test configuration settings"""

    def test_default_settings(self):
        """Test default settings are loaded correctly"""
        settings = Settings()

        assert settings.app_name == "OSSGameForge"
        assert settings.app_version == "0.1.0"
        assert not settings.debug
        assert settings.api_prefix == "/api"
        assert not settings.mock_mode
        assert not settings.use_local_model

    def test_database_url_default(self):
        """Test default database URL"""
        settings = Settings()
        assert settings.database_url == "postgresql://user:password@postgres:5432/ossgameforge"

    def test_minio_settings_default(self):
        """Test default MinIO settings"""
        settings = Settings()

        assert settings.minio_endpoint == "localhost:9000"
        assert settings.minio_access_key == "minioadmin"
        assert settings.minio_secret_key == "minioadmin"
        assert not settings.minio_secure
        assert settings.minio_bucket == "ossgameforge"

    def test_security_settings_default(self):
        """Test default security settings"""
        settings = Settings()

        assert settings.secret_key == "your-secret-key-change-in-production"
        assert settings.algorithm == "HS256"
        assert settings.access_token_expire_minutes == 30

    def test_cors_origins_default(self):
        """Test default CORS origins"""
        settings = Settings()

        assert "http://localhost:3000" in settings.cors_origins
        assert "http://localhost:5173" in settings.cors_origins

    def test_file_upload_settings(self):
        """Test file upload configuration"""
        settings = Settings()

        assert settings.max_upload_size == 100 * 1024 * 1024  # 100MB
        assert "image/jpeg" in settings.allowed_image_types
        assert "image/png" in settings.allowed_image_types
        assert "audio/mpeg" in settings.allowed_audio_types
        assert "video/mp4" in settings.allowed_video_types

    @patch.dict(os.environ, {"MOCK_MODE": "true", "USE_LOCAL_MODEL": "true"})
    def test_environment_override(self):
        """Test settings can be overridden by environment variables"""
        settings = Settings()

        assert settings.mock_mode
        assert settings.use_local_model

    @patch.dict(os.environ, {"DATABASE_URL": "postgresql://test:test@localhost:5432/testdb"})
    def test_database_url_override(self):
        """Test database URL can be overridden"""
        settings = Settings()

        assert settings.database_url == "postgresql://test:test@localhost:5432/testdb"

    @patch.dict(os.environ, {"MAX_UPLOAD_SIZE": "52428800"})  # 50MB
    def test_numeric_environment_override(self):
        """Test numeric settings can be overridden"""
        settings = Settings()

        assert settings.max_upload_size == 52428800

    def test_model_configuration(self):
        """Test model configuration settings"""
        settings = Settings()

        assert settings.model_endpoint is None
        assert settings.model_timeout == 60
        assert settings.model_max_retries == 3

    def test_background_task_timeout(self):
        """Test background task timeout setting"""
        settings = Settings()

        assert settings.background_task_timeout == 300  # 5 minutes
