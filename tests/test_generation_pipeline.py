"""
Comprehensive tests for the generation pipeline

Tests the entire generation flow including:
- Golden sample loading and selection
- Fallback mechanisms
- Inference client functionality
- Generation API endpoints
- Database logging
"""
import pytest
import asyncio
import json
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone
from uuid import uuid4

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

# Set environment for testing
os.environ["USE_LOCAL_MODEL"] = "false"
os.environ["MOCK_MODE"] = "false"

from app.main import app
from app.database import get_db
from app.models.core_models import GenerationLog, Scene
from app.services.inference_client import InferenceClient
from app.services.context_builder import context_builder
from app.services.postprocessor import postprocessor

client = TestClient(app)


class TestGoldenSampleLoading:
    """Test golden sample loading and management"""
    
    def test_golden_samples_exist(self):
        """Verify all golden sample files exist"""
        samples_dir = Path(__file__).parent.parent / "backend" / "app" / "golden_samples"
        assert samples_dir.exists(), "Golden samples directory does not exist"
        
        expected_samples = [
            "sample_simple_geometry.json",
            "sample_asset_intensive.json",
            "sample_complex_structure.json"
        ]
        
        for sample_name in expected_samples:
            sample_path = samples_dir / sample_name
            assert sample_path.exists(), f"Golden sample {sample_name} not found"
            
            # Verify it's valid JSON
            with open(sample_path) as f:
                data = json.load(f)
                assert "id" in data
                assert "scene_name" in data
                # Either entities or layers should be present
                assert "entities" in data or "layers" in data, f"Sample {sample_name} must have entities or layers"
    
    def test_inference_client_loads_samples(self):
        """Test that InferenceClient properly loads golden samples"""
        client = InferenceClient()
        assert len(client.golden_samples) >= 3, "Should load at least 3 golden samples"
        
        # Check sample structure
        for sample in client.golden_samples:
            assert "name" in sample
            assert "keywords" in sample
            assert "complexity" in sample
            assert "data" in sample
            assert sample["complexity"] in [0, 0.5, 1, 2, 3]
    
    def test_list_golden_samples(self):
        """Test listing available golden samples"""
        client = InferenceClient()
        samples = client.list_golden_samples()
        
        assert len(samples) >= 3
        for sample in samples:
            assert "name" in sample
            assert "complexity" in sample
            assert "description" in sample
            assert "keywords" in sample
    
    def test_load_specific_sample(self):
        """Test loading a specific golden sample by name"""
        client = InferenceClient()
        
        # Test loading existing sample
        sample = client.load_golden_sample("sample_simple_geometry")
        assert sample is not None
        assert "scene_name" in sample
        assert sample["scene_name"] == "Simple Block Test"
        
        # Test loading non-existent sample
        sample = client.load_golden_sample("non_existent_sample")
        assert sample is None


class TestIntelligentSampleSelection:
    """Test the intelligent golden sample selection based on prompts"""
    
    def test_simple_prompt_selection(self):
        """Test that simple prompts select the simple geometry sample"""
        client = InferenceClient()
        
        test_prompts = [
            "create a simple platform game",
            "basic geometry test",
            "minimal block level"
        ]
        
        for prompt in test_prompts:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            assert "simple" in sample_name.lower() or result["scene_name"] == "Simple Block Test"
    
    def test_asset_prompt_selection(self):
        """Test that asset-related prompts select the asset intensive sample"""
        client = InferenceClient()
        
        test_prompts = [
            "create a level with textures and sprites",
            "forest background with audio",
            "detailed asset-rich scene"
        ]
        
        for prompt in test_prompts:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            assert "asset" in sample_name.lower() or "Forest" in result.get("scene_name", "")
    
    def test_complex_prompt_selection(self):
        """Test that complex prompts select the complex structure sample"""
        client = InferenceClient()
        
        test_prompts = [
            "create a complex puzzle with layers",
            "advanced scene with triggers and events",
            "nested structure with scripts"
        ]
        
        for prompt in test_prompts:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            assert "complex" in sample_name.lower() or "Layered" in result.get("scene_name", "")
    
    def test_no_match_random_selection(self):
        """Test that prompts with no keywords still get a valid sample"""
        client = InferenceClient()
        
        context = {"engineered_prompt": "xyzabc random words qwerty"}
        result, sample_name = client._use_fallback_sample(context)
        
        assert result is not None
        # Should be one of our valid samples
        valid_samples = [
            "sample_simple_geometry", 
            "sample_asset_intensive", 
            "sample_complex_structure",
            "sample_minimal_empty",
            "sample_single_entity"
        ]
        assert sample_name in valid_samples


class TestGenerationPipeline:
    """Test the complete generation pipeline"""
    
    @pytest.mark.asyncio
    async def test_full_generation_flow(self):
        """Test the complete generation flow with fallback"""
        client = InferenceClient()
        
        # Build context
        context = context_builder.build_generation_prompt(
            user_prompt="Create a simple platformer level",
            project_id="test_project_001",
            style="platformer"
        )
        
        # Generate scene
        result = await client.generate_scene(context)
        
        assert "scene" in result
        assert "metadata" in result
        assert result["metadata"]["status"] in ["cached_fallback", "success"]
        assert result["metadata"]["latency_ms"] > 0
        
        # Process the scene
        processed = postprocessor.process_scene(
            result["scene"],
            "test_project_001"
        )
        
        assert postprocessor.validate_scene(processed)
        assert processed["project_id"] == "test_project_001"
    
    @pytest.mark.asyncio
    async def test_generation_with_assets(self):
        """Test generation with asset references"""
        client = InferenceClient()
        
        test_assets = [
            {"id": "asset1", "type": "image", "path": "/assets/player.png"},
            {"id": "asset2", "type": "audio", "path": "/assets/jump.wav"}
        ]
        
        context = context_builder.build_generation_prompt(
            user_prompt="Create a level with these assets",
            project_id="test_project_002",
            assets=test_assets
        )
        
        result = await client.generate_scene(context)
        
        assert result["metadata"]["status"] in ["cached_fallback", "success"]
        
        # Process with assets
        processed = postprocessor.process_scene(
            result["scene"],
            "test_project_002",
            test_assets
        )
        
        assert "assets" in processed or len(test_assets) == 0


class TestFallbackMechanisms:
    """Test the resilience and fallback mechanisms"""
    
    @pytest.mark.asyncio
    async def test_model_connection_failure_fallback(self):
        """Test fallback when model connection fails"""
        client = InferenceClient()
        client.use_local_model = True
        
        # Mock httpx to simulate connection failure
        with patch("app.services.inference_client.httpx.AsyncClient") as mock_client:
            mock_client.return_value.__aenter__.return_value.post.side_effect = ConnectionError("Cannot connect")
            
            context = {"engineered_prompt": "test prompt", "prompt_hash": "hash123"}
            result = await client.generate_scene(context)
            
            assert result["metadata"]["status"] == "fail_fallback"
            assert "fallback_reason" in result["metadata"]
            assert result["scene"] is not None
    
    @pytest.mark.asyncio
    async def test_model_timeout_fallback(self):
        """Test fallback when model times out"""
        client = InferenceClient()
        client.use_local_model = True
        client.model_timeout = 1  # Very short timeout
        
        with patch("app.services.inference_client.httpx.AsyncClient") as mock_client:
            import httpx
            mock_client.return_value.__aenter__.return_value.post.side_effect = httpx.TimeoutException("Timeout")
            
            context = {"engineered_prompt": "test prompt", "prompt_hash": "hash123"}
            result = await client.generate_scene(context)
            
            assert result["metadata"]["status"] == "fail_fallback"
            assert result["scene"] is not None
    
    def test_error_fallback_scene(self):
        """Test the minimal error fallback scene"""
        client = InferenceClient()
        error_scene = client._get_error_fallback_scene()
        
        assert error_scene is not None
        assert "id" in error_scene
        assert "entities" in error_scene
        assert len(error_scene["entities"]) >= 1
        assert error_scene["entities"][0]["type"] == "player"
    
    @pytest.mark.asyncio
    async def test_no_golden_samples_fallback(self):
        """Test behavior when no golden samples are loaded"""
        client = InferenceClient()
        client.golden_samples = []  # Clear samples
        
        context = {"engineered_prompt": "test prompt"}
        result, sample_name = client._use_fallback_sample(context)
        
        assert sample_name == "error_fallback"
        assert result is not None


class TestGenerationAPI:
    """Test the generation API endpoints"""
    
    def test_generation_endpoint_with_fallback(self):
        """Test the /generate endpoint with fallback mode"""
        response = client.post(
            "/api/generation/",
            json={
                "prompt": "Create a simple platformer level",
                "project_id": "test_proj_001",
                "style": "platformer"
            }
        )
        
        assert response.status_code == 200
        data = response.json()
        
        assert "scene_id" in data
        assert "scene" in data
        assert "generation_time" in data
        assert "metadata" in data
        assert data["metadata"]["status"] in ["cached_fallback", "success", "fail_fallback"]
    
    def test_generation_status_endpoint(self):
        """Test the /generate/status endpoint"""
        response = client.get("/api/generation/status")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "use_local_model" in data
        assert "fallback_samples_loaded" in data
        assert "golden_samples" in data
        assert "status" in data
        assert "statistics" in data
        assert data["fallback_samples_loaded"] >= 3
    
    def test_list_samples_endpoint(self):
        """Test the /generate/samples endpoint"""
        response = client.get("/api/generation/samples")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "samples" in data
        assert "total" in data
        assert data["total"] >= 3
        
        for sample in data["samples"]:
            assert "name" in sample
            assert "complexity" in sample
            assert "description" in sample
    
    def test_get_specific_sample_endpoint(self):
        """Test getting a specific golden sample via API"""
        response = client.get("/api/generation/samples/sample_simple_geometry")
        
        assert response.status_code == 200
        data = response.json()
        
        assert "scene_name" in data
        assert data["scene_name"] == "Simple Block Test"
        assert "entities" in data
    
    def test_get_nonexistent_sample_endpoint(self):
        """Test getting a non-existent sample returns 404"""
        response = client.get("/api/generation/samples/non_existent")
        
        assert response.status_code == 404


class TestPerformanceAndLatency:
    """Test performance characteristics and latency"""
    
    @pytest.mark.asyncio
    async def test_fallback_mode_latency(self):
        """Test that fallback mode returns quickly"""
        import time
        
        client = InferenceClient()
        client.use_local_model = False
        
        context = {"engineered_prompt": "test", "prompt_hash": "hash"}
        
        start = time.time()
        result = await client.generate_scene(context)
        elapsed = time.time() - start
        
        assert elapsed < 1.0, "Fallback mode should return in less than 1 second"
        assert result["metadata"]["latency_ms"] < 1000
    
    def test_statistics_tracking(self):
        """Test that the inference client tracks statistics"""
        client = InferenceClient()
        initial_requests = client.stats["total_requests"]
        
        # Make a request
        asyncio.run(client.generate_scene({"engineered_prompt": "test"}))
        
        assert client.stats["total_requests"] == initial_requests + 1
        assert client.stats["fallback_uses"] > 0
        assert client.stats["last_request_time"] is not None


class TestSceneValidation:
    """Test scene validation and processing"""
    
    def test_validate_golden_samples(self):
        """Test that all golden samples pass validation"""
        samples_dir = Path(__file__).parent.parent / "backend" / "app" / "golden_samples"
        
        for sample_file in samples_dir.glob("sample_*.json"):
            with open(sample_file) as f:
                scene = json.load(f)
            
            # Check basic structure
            assert "id" in scene, f"Sample {sample_file.name} missing 'id'"
            assert "scene_name" in scene, f"Sample {sample_file.name} missing 'scene_name'"
            
            # Check for entities or layers (complex structures may use layers)
            has_entities = "entities" in scene
            has_layers = "layers" in scene
            assert has_entities or has_layers, f"Sample {sample_file.name} must have entities or layers"
            
            # If it has the standard structure, validate with postprocessor
            if has_entities:
                processed = postprocessor.process_scene(scene, "test_project")
                assert postprocessor.validate_scene(processed), f"Sample {sample_file.name} failed validation"
    
    def test_scene_enhancement(self):
        """Test that scenes are properly enhanced"""
        scene = {
            "id": "test_scene",
            "scene_name": "Test",
            "style": "platformer",
            "entities": [
                {
                    "id": "player1",
                    "type": "player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 32, "height": 48}
                }
            ]
        }
        
        enhanced = postprocessor.enhance_scene(scene)
        
        # Check enhancements were applied
        assert enhanced["entities"][0].get("properties") is not None
        if "physics" in enhanced["entities"][0]["properties"]:
            assert "mass" in enhanced["entities"][0]["properties"]["physics"]


class TestDatabaseLogging:
    """Test database logging functionality"""
    
    @pytest.mark.asyncio
    async def test_generation_logging(self, db_session):
        """Test that generations are logged to database"""
        from app.routers.generation import log_generation
        
        await log_generation(
            db=db_session,
            user_id="test_user",
            input_hash="input123",
            prompt_hash="prompt456",
            model_version="fallback",
            status="cached_fallback",
            latency_ms=100,
            request_payload={"prompt": "test"},
            response_payload={"scene": "data"}
        )
        
        # Query the log
        log = db_session.query(GenerationLog).filter_by(input_hash="input123").first()
        
        assert log is not None
        assert log.user_id == "test_user"
        assert log.status == "cached_fallback"
        assert log.latency_ms == 100
    
    @pytest.mark.asyncio
    async def test_scene_saving(self, db_session):
        """Test that generated scenes are saved to database"""
        from app.routers.generation import save_scene_to_db
        
        scene_data = {
            "scene_name": "Test Scene",
            "style": "platformer",
            "entities": []
        }
        
        await save_scene_to_db(
            db=db_session,
            project_id="test_project",
            scene_data=scene_data
        )
        
        # Query the scene
        scene = db_session.query(Scene).filter_by(project_id="test_project").first()
        
        assert scene is not None
        assert scene.name == "Test Scene"
        assert scene.style == "platformer"


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    @pytest.mark.asyncio
    async def test_empty_prompt(self):
        """Test handling of empty prompts"""
        client = InferenceClient()
        context = {"engineered_prompt": "", "prompt_hash": "empty"}
        
        result = await client.generate_scene(context)
        assert result["scene"] is not None
    
    @pytest.mark.asyncio
    async def test_very_long_prompt(self):
        """Test handling of very long prompts"""
        client = InferenceClient()
        long_prompt = "test " * 1000  # Very long prompt
        context = {"engineered_prompt": long_prompt, "prompt_hash": "long"}
        
        result = await client.generate_scene(context)
        assert result["scene"] is not None
    
    def test_malformed_golden_sample_handling(self):
        """Test handling of malformed golden samples"""
        client = InferenceClient()
        
        # Add a malformed sample
        client.golden_samples.append({
            "name": "malformed",
            "keywords": [],
            "complexity": 1,
            "data": {"invalid": "structure"}  # Missing required fields
        })
        
        # Should still work with other samples
        context = {"engineered_prompt": "simple test"}
        result, sample_name = client._use_fallback_sample(context)
        
        assert result is not None
        assert sample_name != "malformed"


@pytest.fixture
def db_session():
    """Create a test database session"""
    from app.database import SessionLocal
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])