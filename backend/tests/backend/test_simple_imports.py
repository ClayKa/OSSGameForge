"""
Simple tests to verify imports and basic functionality
"""
import sys
import os
sys.path.insert(0, '/app')

def test_import_schemas():
    """Test that schemas can be imported"""
    from app.schemas.project import ProjectCreate
    from app.schemas.asset import AssetType
    from app.schemas.generation import GameStyle
    from app.schemas.export import ExportEngine
    
    assert ProjectCreate is not None
    assert AssetType.IMAGE == "image"
    assert GameStyle.PLATFORMER == "platformer"
    assert ExportEngine.HTML5 == "html5"

def test_import_config():
    """Test that config can be imported"""
    from app.config import Settings
    
    settings = Settings()
    assert settings.app_name == "OSSGameForge"
    assert settings.app_version == "0.1.0"

def test_import_routers():
    """Test that routers can be imported"""
    from app.routers import projects, assets, generation, export
    
    assert projects.router is not None
    assert assets.router is not None
    assert generation.router is not None
    assert export.router is not None

def test_mock_mode_env():
    """Test mock mode environment variable"""
    os.environ['MOCK_MODE'] = 'true'
    from app.config import Settings
    
    settings = Settings()
    assert settings.mock_mode is True

def test_api_endpoints_exist():
    """Test that API endpoints are registered"""
    from app.main import app
    
    routes = [route.path for route in app.routes]
    
    assert "/health" in routes
    assert "/" in routes
    assert "/api/projects/" in routes or "/api/projects/{project_id}" in routes
    assert "/api/generate" in routes

if __name__ == "__main__":
    test_import_schemas()
    print("✅ Schema imports work")
    
    test_import_config()
    print("✅ Config imports work")
    
    test_import_routers()
    print("✅ Router imports work")
    
    test_mock_mode_env()
    print("✅ Environment variables work")
    
    test_api_endpoints_exist()
    print("✅ API endpoints registered")
    
    print("\n🎉 All simple tests passed!")