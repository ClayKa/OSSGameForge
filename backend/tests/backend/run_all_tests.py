#!/usr/bin/env python
"""
Run all backend tests without pytest dependencies issues
"""
import os
import sys

sys.path.insert(0, '/app')

def run_test_imports():
    """Test imports and basic functionality"""
    print("\n" + "="*60)
    print("RUNNING: Import and Basic Tests")
    print("="*60)

    from test_simple_imports import (
        test_api_endpoints_exist,
        test_import_config,
        test_import_routers,
        test_import_schemas,
        test_mock_mode_env,
    )

    tests_passed = 0
    tests_failed = 0

    try:
        test_import_schemas()
        print("✅ Schema imports test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Schema imports test FAILED: {e}")
        tests_failed += 1

    try:
        test_import_config()
        print("✅ Config imports test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Config imports test FAILED: {e}")
        tests_failed += 1

    try:
        test_import_routers()
        print("✅ Router imports test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Router imports test FAILED: {e}")
        tests_failed += 1

    try:
        test_mock_mode_env()
        print("✅ Environment variables test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Environment variables test FAILED: {e}")
        tests_failed += 1

    try:
        test_api_endpoints_exist()
        print("✅ API endpoints test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ API endpoints test FAILED: {e}")
        tests_failed += 1

    return tests_passed, tests_failed


def run_schema_tests():
    """Test schema validation"""
    print("\n" + "="*60)
    print("RUNNING: Schema Validation Tests")
    print("="*60)

    tests_passed = 0
    tests_failed = 0

    # Test Project schemas
    try:
        from app.schemas.project import ProjectCreate, ProjectResponse

        # Valid project
        project = ProjectCreate(name="Test Project", description="Test")
        assert project.name == "Test Project"
        print("✅ ProjectCreate schema test PASSED")
        tests_passed += 1

        # Project response
        response = ProjectResponse(
            id="proj_001",
            name="Test",
            owner="user",
            created_at="2024-01-01T00:00:00Z",
            updated_at="2024-01-01T00:00:00Z",
            assets_count=0,
            scenes_count=0
        )
        assert response.id == "proj_001"
        print("✅ ProjectResponse schema test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Project schema tests FAILED: {e}")
        tests_failed += 2

    # Test Asset schemas
    try:
        from app.schemas.asset import AssetStatus, AssetType, AssetUploadResponse

        assert AssetType.IMAGE == "image"
        assert AssetStatus.PROCESSING == "processing"

        upload_response = AssetUploadResponse(
            asset_id="asset_001",
            status="processing",
            message="Test"
        )
        assert upload_response.asset_id == "asset_001"
        print("✅ Asset schema tests PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Asset schema tests FAILED: {e}")
        tests_failed += 1

    # Test Generation schemas
    try:
        from app.schemas.generation import EntityType, GameStyle, GenerationRequest, Position, Size

        assert GameStyle.PLATFORMER == "platformer"
        assert EntityType.PLAYER == "player"

        pos = Position(x=100, y=200)
        assert pos.x == 100

        size = Size(width=50, height=100)
        assert size.width == 50

        request = GenerationRequest(
            prompt="Create a level",
            project_id="proj_001"
        )
        assert request.prompt == "Create a level"
        print("✅ Generation schema tests PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Generation schema tests FAILED: {e}")
        tests_failed += 1

    # Test Export schemas
    try:
        from app.schemas.export import ExportEngine, ExportRequest

        assert ExportEngine.HTML5 == "html5"

        request = ExportRequest(scene_id="scene_001")
        assert request.scene_id == "scene_001"
        assert request.include_assets is True  # default
        print("✅ Export schema tests PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Export schema tests FAILED: {e}")
        tests_failed += 1

    return tests_passed, tests_failed


def run_api_tests():
    """Test API endpoints"""
    print("\n" + "="*60)
    print("RUNNING: API Endpoint Tests")
    print("="*60)

    from app.main import app
    from fastapi.testclient import TestClient

    client = TestClient(app)
    tests_passed = 0
    tests_failed = 0

    # Test health endpoint
    try:
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        print("✅ Health endpoint test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Health endpoint test FAILED: {e}")
        tests_failed += 1

    # Test root endpoint
    try:
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        print("✅ Root endpoint test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Root endpoint test FAILED: {e}")
        tests_failed += 1

    # Test API docs
    try:
        response = client.get("/docs")
        assert response.status_code == 200
        print("✅ API docs endpoint test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ API docs endpoint test FAILED: {e}")
        tests_failed += 1

    # Test OpenAPI schema
    try:
        response = client.get("/openapi.json")
        assert response.status_code == 200
        data = response.json()
        assert "openapi" in data
        assert "paths" in data
        print("✅ OpenAPI schema test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ OpenAPI schema test FAILED: {e}")
        tests_failed += 1

    return tests_passed, tests_failed


def run_mock_api_tests():
    """Test mock API functionality"""
    print("\n" + "="*60)
    print("RUNNING: Mock API Tests")
    print("="*60)

    os.environ['MOCK_MODE'] = 'true'

    from app.config import settings
    from app.main import app
    from fastapi.testclient import TestClient

    # Force reload settings
    settings.mock_mode = True

    client = TestClient(app)
    tests_passed = 0
    tests_failed = 0

    # Test project creation in mock mode
    try:
        response = client.post("/api/projects/", json={
            "name": "Test Project",
            "description": "Test Description"
        })
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Test Project"
        print("✅ Mock project creation test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Mock project creation test FAILED: {e}")
        tests_failed += 1

    # Test generation in mock mode
    try:
        response = client.post("/api/generate", json={
            "prompt": "Create a test level",
            "project_id": "proj_001"
        })
        assert response.status_code == 200
        data = response.json()
        assert "scene_id" in data
        assert "scene" in data
        print("✅ Mock generation test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Mock generation test FAILED: {e}")
        tests_failed += 1

    # Test asset upload with consent
    try:
        files = {'file': ('test.txt', b'test content', 'text/plain')}
        data = {'user_consent': 'true'}
        response = client.post(
            "/api/projects/proj_001/assets",
            files=files,
            data=data
        )
        assert response.status_code == 202
        result = response.json()
        assert "asset_id" in result
        print("✅ Mock asset upload test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Mock asset upload test FAILED: {e}")
        tests_failed += 1

    # Test asset upload without consent (should fail)
    try:
        files = {'file': ('test.txt', b'test content', 'text/plain')}
        data = {'user_consent': 'false'}
        response = client.post(
            "/api/projects/proj_001/assets",
            files=files,
            data=data
        )
        assert response.status_code == 400
        print("✅ Consent validation test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Consent validation test FAILED: {e}")
        tests_failed += 1

    # Test export
    try:
        response = client.post("/api/export?engine=html5", json={
            "scene_id": "scene_001",
            "include_assets": True
        })
        assert response.status_code == 200
        print("✅ Mock export test PASSED")
        tests_passed += 1
    except Exception as e:
        print(f"❌ Mock export test FAILED: {e}")
        tests_failed += 1

    return tests_passed, tests_failed


def main():
    """Run all tests and generate summary"""
    print("\n" + "="*70)
    print("OSSGameForge - Complete Test Suite")
    print("="*70)

    total_passed = 0
    total_failed = 0

    # Run import tests
    passed, failed = run_test_imports()
    total_passed += passed
    total_failed += failed

    # Run schema tests
    passed, failed = run_schema_tests()
    total_passed += passed
    total_failed += failed

    # Run API tests
    passed, failed = run_api_tests()
    total_passed += passed
    total_failed += failed

    # Run mock API tests
    passed, failed = run_mock_api_tests()
    total_passed += passed
    total_failed += failed

    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Total Tests Run: {total_passed + total_failed}")
    print(f"✅ Passed: {total_passed}")
    print(f"❌ Failed: {total_failed}")
    print(f"Pass Rate: {(total_passed/(total_passed+total_failed)*100):.1f}%")

    if total_failed == 0:
        print("\n🎉 ALL TESTS PASSED! The backend is fully functional!")
        return 0
    else:
        print(f"\n⚠️  {total_failed} tests failed. Please review the failures above.")
        return 1


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
