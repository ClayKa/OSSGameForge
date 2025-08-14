"""
Pytest configuration and shared fixtures
"""
import pytest
import asyncio
from typing import Generator, AsyncGenerator
from unittest.mock import MagicMock
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'backend'))

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.pool import StaticPool

# Import app dependencies
from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.config import settings

# Test database URL (in-memory SQLite for speed)
TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope="session")
def event_loop():
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()

@pytest.fixture(scope="function")
def test_db_engine():
    """Create a test database engine"""
    engine = create_engine(
        TEST_DATABASE_URL,
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    yield engine
    Base.metadata.drop_all(bind=engine)
    engine.dispose()

@pytest.fixture(scope="function")
def test_db_session(test_db_engine) -> Generator[Session, None, None]:
    """Create a test database session"""
    TestingSessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=test_db_engine
    )
    session = TestingSessionLocal()
    yield session
    session.close()

@pytest.fixture(scope="function")
def test_client(test_db_session) -> TestClient:
    """Create a test client with overridden database dependency"""
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()

@pytest.fixture
def mock_minio_client():
    """Mock MinIO client for storage tests"""
    mock_client = MagicMock()
    mock_client.bucket_exists.return_value = True
    mock_client.put_object.return_value = MagicMock()
    mock_client.get_object.return_value = MagicMock()
    return mock_client

@pytest.fixture
def sample_image_file():
    """Create a sample image file for testing"""
    from io import BytesIO
    from PIL import Image
    
    # Create a simple RGB image
    img = Image.new('RGB', (100, 100), color='red')
    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return {
        "file": img_bytes,
        "filename": "test_image.png",
        "content_type": "image/png"
    }

@pytest.fixture
def sample_audio_file():
    """Create a sample audio file mock for testing"""
    return {
        "file": BytesIO(b"fake audio content"),
        "filename": "test_audio.mp3",
        "content_type": "audio/mpeg"
    }

@pytest.fixture
def mock_settings():
    """Override settings for testing"""
    test_settings = settings.copy()
    test_settings.mock_mode = True
    test_settings.use_local_model = False
    test_settings.database_url = TEST_DATABASE_URL
    return test_settings

@pytest.fixture
def auth_headers():
    """Mock authentication headers"""
    return {"Authorization": "Bearer test-token"}

@pytest.fixture
async def async_client(test_db_session):
    """Async test client for async endpoint testing"""
    from httpx import AsyncClient
    
    def override_get_db():
        try:
            yield test_db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    
    async with AsyncClient(app=app, base_url="http://test") as client:
        yield client
    
    app.dependency_overrides.clear()