"""
Tests for Pydantic schemas
"""
import pytest
from pydantic import ValidationError
from datetime import datetime

from app.schemas.project import ProjectCreate, ProjectResponse, ProjectUpdate
from app.schemas.asset import (
    AssetType, AssetStatus, AssetUploadResponse, AssetResponse
)
from app.schemas.generation import (
    GameStyle, EntityType, Position, Size, Entity, 
    SceneMetadata, Scene, GenerationRequest, GenerationResponse
)
from app.schemas.export import ExportEngine, ExportRequest


class TestProjectSchemas:
    """Test project schemas"""
    
    def test_project_create_valid(self):
        """Test creating a valid project"""
        data = {
            "name": "Test Project",
            "description": "A test project"
        }
        project = ProjectCreate(**data)
        assert project.name == "Test Project"
        assert project.description == "A test project"
    
    def test_project_create_without_description(self):
        """Test creating a project without description"""
        data = {"name": "Test Project"}
        project = ProjectCreate(**data)
        assert project.name == "Test Project"
        assert project.description is None
    
    def test_project_create_invalid_name(self):
        """Test creating a project with invalid name"""
        with pytest.raises(ValidationError):
            ProjectCreate(name="", description="Test")
        
        with pytest.raises(ValidationError):
            ProjectCreate(name="a" * 101, description="Test")
    
    def test_project_response(self):
        """Test project response schema"""
        data = {
            "id": "proj_001",
            "name": "Test Project",
            "description": "Test",
            "owner": "user_001",
            "created_at": "2024-01-01T00:00:00Z",
            "updated_at": "2024-01-01T00:00:00Z",
            "assets_count": 5,
            "scenes_count": 2
        }
        project = ProjectResponse(**data)
        assert project.id == "proj_001"
        assert project.assets_count == 5
        assert project.scenes_count == 2
    
    def test_project_update(self):
        """Test project update schema"""
        data = {"name": "Updated Name"}
        update = ProjectUpdate(**data)
        assert update.name == "Updated Name"
        assert update.description is None


class TestAssetSchemas:
    """Test asset schemas"""
    
    def test_asset_type_enum(self):
        """Test asset type enumeration"""
        assert AssetType.IMAGE == "image"
        assert AssetType.AUDIO == "audio"
        assert AssetType.VIDEO == "video"
        assert AssetType.MODEL == "model"
    
    def test_asset_status_enum(self):
        """Test asset status enumeration"""
        assert AssetStatus.PROCESSING == "processing"
        assert AssetStatus.PROCESSED == "processed"
        assert AssetStatus.FAILED == "failed"
    
    def test_asset_upload_response(self):
        """Test asset upload response schema"""
        data = {
            "asset_id": "asset_001",
            "status": "processing",
            "message": "Upload initiated"
        }
        response = AssetUploadResponse(**data)
        assert response.asset_id == "asset_001"
        assert response.status == AssetStatus.PROCESSING
    
    def test_asset_response(self):
        """Test asset response schema"""
        data = {
            "id": "asset_001",
            "project_id": "proj_001",
            "filename": "test.png",
            "path": "/assets/test.png",
            "type": "image",
            "status": "processed",
            "metadata": {"width": 100, "height": 100},
            "consent_hash": "abc123",
            "exif_stripped": True,
            "created_at": "2024-01-01T00:00:00Z"
        }
        asset = AssetResponse(**data)
        assert asset.id == "asset_001"
        assert asset.type == AssetType.IMAGE
        assert asset.status == AssetStatus.PROCESSED
        assert asset.exif_stripped is True


class TestGenerationSchemas:
    """Test generation schemas"""
    
    def test_game_style_enum(self):
        """Test game style enumeration"""
        assert GameStyle.PLATFORMER == "platformer"
        assert GameStyle.SHOOTER == "shooter"
        assert GameStyle.PUZZLE == "puzzle"
        assert GameStyle.RPG == "rpg"
    
    def test_entity_type_enum(self):
        """Test entity type enumeration"""
        assert EntityType.PLAYER == "player"
        assert EntityType.PLATFORM == "platform"
        assert EntityType.ENEMY == "enemy"
        assert EntityType.COLLECTIBLE == "collectible"
        assert EntityType.GOAL == "goal"
        assert EntityType.OBSTACLE == "obstacle"
    
    def test_position_schema(self):
        """Test position schema"""
        pos = Position(x=100.5, y=200.5)
        assert pos.x == 100.5
        assert pos.y == 200.5
    
    def test_size_schema(self):
        """Test size schema"""
        size = Size(width=50, height=100)
        assert size.width == 50
        assert size.height == 100
    
    def test_entity_schema(self):
        """Test entity schema"""
        data = {
            "id": "entity_001",
            "type": "player",
            "name": "Player 1",
            "position": {"x": 100, "y": 200},
            "size": {"width": 50, "height": 50},
            "sprite": "/assets/player.png",
            "color": "#FF0000",
            "physics": {
                "gravity": True,
                "collision": True,
                "static": False,
                "mass": 1.0
            },
            "properties": {"health": 100}
        }
        entity = Entity(**data)
        assert entity.id == "entity_001"
        assert entity.type == EntityType.PLAYER
        assert entity.position.x == 100
        assert entity.physics.gravity is True
    
    def test_scene_metadata(self):
        """Test scene metadata schema"""
        data = {
            "width": 1920,
            "height": 1080,
            "background_color": "#87CEEB",
            "theme": "forest",
            "used_assets": ["asset_001", "asset_002"]
        }
        metadata = SceneMetadata(**data)
        assert metadata.width == 1920
        assert metadata.theme == "forest"
        assert len(metadata.used_assets) == 2
    
    def test_generation_request(self):
        """Test generation request schema"""
        data = {
            "prompt": "Create a platformer level",
            "project_id": "proj_001",
            "assets": ["asset_001"],
            "style": "platformer"
        }
        request = GenerationRequest(**data)
        assert request.prompt == "Create a platformer level"
        assert request.style == GameStyle.PLATFORMER
    
    def test_generation_request_validation(self):
        """Test generation request validation"""
        # Empty prompt should fail
        with pytest.raises(ValidationError):
            GenerationRequest(prompt="", project_id="proj_001")
        
        # Too long prompt should fail
        with pytest.raises(ValidationError):
            GenerationRequest(prompt="a" * 1001, project_id="proj_001")
    
    def test_generation_response(self):
        """Test generation response schema"""
        data = {
            "scene_id": "scene_001",
            "scene": {
                "id": "scene_001",
                "project_id": "proj_001",
                "name": "Test Scene",
                "description": "A test scene",
                "version": "1.0.0",
                "metadata": {
                    "width": 1920,
                    "height": 1080,
                    "background_color": "#87CEEB"
                },
                "entities": [],
                "created_at": "2024-01-01T00:00:00Z"
            },
            "generation_time": 1.5
        }
        response = GenerationResponse(**data)
        assert response.scene_id == "scene_001"
        assert response.generation_time == 1.5


class TestExportSchemas:
    """Test export schemas"""
    
    def test_export_engine_enum(self):
        """Test export engine enumeration"""
        assert ExportEngine.HTML5 == "html5"
        assert ExportEngine.GODOT == "godot"
        assert ExportEngine.UNITY == "unity"
    
    def test_export_request(self):
        """Test export request schema"""
        data = {
            "scene_id": "scene_001",
            "include_assets": True
        }
        request = ExportRequest(**data)
        assert request.scene_id == "scene_001"
        assert request.include_assets is True
    
    def test_export_request_defaults(self):
        """Test export request with defaults"""
        data = {"scene_id": "scene_001"}
        request = ExportRequest(**data)
        assert request.scene_id == "scene_001"
        assert request.include_assets is True  # default value