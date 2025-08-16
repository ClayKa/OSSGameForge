"""
Configuration management for OSSGameForge backend
"""

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings with environment variable support
    """

    # Application
    app_name: str = "OSSGameForge"
    app_version: str = "0.1.0"
    debug: bool = False
    # API
    api_prefix: str = "/api"
    mock_mode: bool = Field(default=False)
    use_local_model: bool = Field(default=False)
    # Database
    database_url: str = "postgresql://user:password@postgres:5432/ossgameforge"
    # MinIO/S3
    minio_endpoint: str = "localhost:9000"
    minio_access_key: str = "minioadmin"
    minio_secret_key: str = "minioadmin"
    minio_secure: bool = False
    minio_bucket: str = "ossgameforge"
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    # CORS
    cors_origins: list = ["http://localhost:3000", "http://localhost:5173"]
    # Model Configuration
    model_endpoint: str | None = None
    model_timeout: int = 60
    model_max_retries: int = 3

    # File Upload
    max_upload_size: int = 100 * 1024 * 1024  # 100MB
    allowed_image_types: list = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    allowed_audio_types: list = ["audio/mpeg", "audio/wav", "audio/ogg", "audio/webm"]
    allowed_video_types: list = ["video/mp4", "video/webm", "video/ogg"]
    # Processing
    background_task_timeout: int = 300  # 5 minutes

    class Config:
        env_file = ".env"
        case_sensitive = False

        # Allow reading from environment variables
        @classmethod
        def parse_env_var(cls, field_name: str, raw_val: str):
            if field_name in (
                "cors_origins",
                "allowed_image_types",
                "allowed_audio_types",
                "allowed_video_types",
            ):
                return [x.strip() for x in raw_val.split(",")]
            return raw_val


# Create global settings instance
settings = Settings()
