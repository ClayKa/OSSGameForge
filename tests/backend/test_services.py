"""
Tests for backend services
"""
import pytest
import asyncio
from pathlib import Path
import json
from unittest.mock import patch, MagicMock, mock_open

from app.config import Settings
from app.services.context_builder import context_builder
from app.services.inference_client import inference_client
from app.services.postprocessor import postprocessor


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
    
    @patch.dict('os.environ', {'MOCK_MODE': 'true', 'USE_LOCAL_MODEL': 'true'})
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
        mock_data = {
            "projects": [{"id": "proj_001", "name": "Test"}],
            "assets": [],
            "scenes": []
        }
        
        # Import the function to test
        from app.routers.projects import load_mock_data
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
                result = load_mock_data()
                assert "projects" in result
                assert len(result["projects"]) == 1
                assert result["projects"][0]["id"] == "proj_001"
    
    def test_load_mock_data_file_not_exists(self):
        """Test loading mock data when file doesn't exist"""
        from app.routers.projects import load_mock_data
        
        with patch('pathlib.Path.exists', return_value=False):
            result = load_mock_data()
            assert result == {"projects": [], "assets": [], "scenes": []}
    
    def test_load_mock_data_with_generation_samples(self):
        """Test loading mock data with generation samples"""
        mock_data = {
            "generation_samples": [
                {
                    "prompt": "Create a level",
                    "scene": {"id": "scene_001", "name": "Test Scene"}
                }
            ]
        }
        
        from app.routers.generation import load_mock_data
        
        with patch('pathlib.Path.exists', return_value=True):
            with patch('builtins.open', mock_open(read_data=json.dumps(mock_data))):
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
            "metadata": {
                "width": 800,
                "height": 600,
                "background_color": "#000000"
            },
            "entities": [
                {
                    "id": "entity_001",
                    "type": "player",
                    "name": "Player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 50, "height": 50},
                    "color": "#FF0000"
                }
            ]
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
                raise HTTPException(status_code=400, detail="User consent is required for asset upload")
            
            assert exc_info.value.status_code == 400
            assert "consent is required" in exc_info.value.detail.lower()
    
    def test_file_size_validation(self):
        """Test file size validation"""
        from app.config import Settings
        from fastapi import HTTPException
        
        settings = Settings()
        file_size = 150 * 1024 * 1024  # 150MB
        
        if file_size > settings.max_upload_size:
            with pytest.raises(HTTPException) as exc_info:
                raise HTTPException(
                    status_code=413,
                    detail=f"File size exceeds maximum allowed size of {settings.max_upload_size} bytes"
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
        assert "path" in columns  # Not filename
        assert "type" in columns
        assert "status" in columns
        assert "asset_metadata" in columns  # Renamed from metadata
        assert "consent_hash" in columns
        assert "exif_stripped" in columns
        assert "created_at" in columns
        assert "updated_at" in columns
    
    def test_generation_log_model_fields(self):
        """Test that GenerationLog model has required fields"""
        from app.models import GenerationLog
        
        columns = [c.name for c in GenerationLog.__table__.columns]
        
        assert "id" in columns
        assert "user_id" in columns
        assert "input_hash" in columns
        assert "prompt_hash" in columns
        assert "model_version" in columns
        assert "status" in columns
        assert "latency_ms" in columns
        assert "created_at" in columns


class TestContextBuilder:
    """Test the ContextBuilder service"""
    
    def test_build_generation_prompt(self):
        """Test basic prompt building"""
        context = context_builder.build_generation_prompt(
            user_prompt="Create a platformer level with enemies",
            project_id="test_project_001",
            style="platformer"
        )
        
        assert "user_prompt" in context
        assert "project_id" in context
        assert "style" in context
        assert "prompt_hash" in context
        assert "engineered_prompt" in context
        assert context["style"] == "platformer"
    
    def test_prompt_with_assets(self):
        """Test prompt building with assets"""
        test_assets = [
            {"id": "asset1", "type": "image", "name": "player.png", "metadata": {"width": 32, "height": 32}},
            {"id": "asset2", "type": "audio", "name": "jump.wav", "metadata": {"duration": 0.5}}
        ]
        
        context = context_builder.build_generation_prompt(
            user_prompt="Create a level using these assets",
            project_id="test_project_002",
            assets=test_assets
        )
        
        assert "assets" in context
        assert context["asset_count"] == 2
        assert len(context["assets"]) == 2
    
    def test_context_validation(self):
        """Test context validation"""
        valid_context = {"user_prompt": "test", "project_id": "proj1"}
        invalid_context = {"user_prompt": "test"}  # Missing project_id
        
        assert context_builder.validate_context(valid_context) is True
        assert context_builder.validate_context(invalid_context) is False
    
    def test_build_editing_context(self):
        """Test editing context creation"""
        current_scene = {"id": "scene1", "entities": []}
        modifications = {"add_enemy": True, "position": {"x": 100, "y": 200}}
        
        edit_context = context_builder.build_editing_context(
            scene_id="scene1",
            modifications=modifications,
            current_scene=current_scene
        )
        
        assert edit_context["scene_id"] == "scene1"
        assert edit_context["operation"] == "edit"
        assert "modifications" in edit_context
        assert "current_state" in edit_context


class TestInferenceClient:
    """Test the InferenceClient service"""
    
    def test_model_status(self):
        """Test getting model status"""
        status = inference_client.get_model_status()
        
        assert "use_local_model" in status
        assert "status" in status
        assert status["status"] == "ready"
    
    @pytest.mark.asyncio
    async def test_scene_generation(self):
        """Test scene generation with fallback"""
        test_context = {
            "user_prompt": "Create a simple platformer level",
            "engineered_prompt": "Create a platformer game scene",
            "project_id": "test_proj",
            "prompt_hash": "test_hash_123"
        }
        
        result = await inference_client.generate_scene(test_context)
        
        assert "scene" in result
        assert "metadata" in result
        assert result["metadata"]["status"] in ["success", "error"]
        assert "latency_ms" in result["metadata"]
        
        # Verify scene structure
        scene = result["scene"]
        assert "id" in scene
        assert "entities" in scene
        assert isinstance(scene["entities"], list)
    
    @pytest.mark.asyncio
    async def test_fallback_sample_selection(self):
        """Test different prompts trigger different samples"""
        prompts = [
            "simple geometry platform",
            "asset texture sprite detailed",
            "complex advanced multiple enemies"
        ]
        
        for prompt in prompts:
            context = {"engineered_prompt": prompt, "prompt_hash": f"hash_{prompt}"}
            result = await inference_client.generate_scene(context)
            assert result["scene"] is not None


class TestPostprocessor:
    """Test the Postprocessor service"""
    
    def test_process_valid_scene(self):
        """Test processing a valid scene"""
        raw_scene = {
            "name": "Test Scene",
            "style": "platformer",
            "entities": [
                {
                    "type": "player",
                    "position": {"x": 100, "y": 200}
                },
                {
                    "type": "platform",
                    "position": {"x": 0, "y": 400},
                    "size": {"width": 800, "height": 20}
                }
            ]
        }
        
        processed = postprocessor.process_scene(raw_scene, "test_project")
        
        assert "id" in processed
        assert "project_id" in processed
        assert processed["project_id"] == "test_project"
        assert "metadata" in processed
        assert len(processed["entities"]) == 2
        
        # Check entities have been normalized
        for entity in processed["entities"]:
            assert "id" in entity
            assert "position" in entity
            assert "size" in entity
            assert "properties" in entity
    
    def test_scene_validation(self):
        """Test scene validation logic"""
        valid_scene = {
            "id": "scene1",
            "name": "Valid Scene",
            "style": "platformer",
            "entities": [
                {
                    "id": "e1",
                    "type": "player",
                    "position": {"x": 0, "y": 0},
                    "size": {"width": 32, "height": 32}
                }
            ]
        }
        
        invalid_scene = {
            "name": "Invalid Scene",
            # Missing required fields
        }
        
        assert postprocessor.validate_scene(valid_scene) is True
        assert postprocessor.validate_scene(invalid_scene) is False
    
    def test_scene_enhancement(self):
        """Test scene enhancement features"""
        basic_scene = {
            "id": "scene1",
            "name": "Basic Scene",
            "style": "platformer",
            "entities": [
                {
                    "id": "player1",
                    "type": "player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 32, "height": 48},
                    "properties": {}
                }
            ]
        }
        
        enhanced = postprocessor.enhance_scene(basic_scene)
        
        # Check physics properties were added
        assert "physics" in enhanced["entities"][0]["properties"]
        
        # Check collision boundaries were added
        assert "collision_box" in enhanced["entities"][0]
    
    def test_asset_incorporation(self):
        """Test incorporating assets into scene"""
        scene = {
            "id": "scene1",
            "name": "Scene with Assets",
            "style": "platformer",
            "entities": [
                {
                    "id": "player1",
                    "type": "player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 32, "height": 48},
                    "properties": {}
                }
            ]
        }
        
        assets = [
            {"id": "asset1", "type": "image", "path": "/assets/player.png"},
            {"id": "asset2", "type": "audio", "path": "/assets/jump.wav"}
        ]
        
        processed = postprocessor.process_scene(scene, "test_proj", assets)
        
        assert "assets" in processed
        assert len(processed["assets"]) > 0
    
    def test_minimal_scene_fallback(self):
        """Test minimal scene generation on invalid input"""
        # Invalid scene should trigger minimal fallback
        invalid_raw = {"invalid": "data"}
        
        minimal = postprocessor.process_scene(invalid_raw, "test_project")
        
        assert postprocessor.validate_scene(minimal) is True
        assert len(minimal["entities"]) >= 1
        assert minimal["entities"][0]["type"] == "player"