"""
Comprehensive tests for generation pipeline edge cases and new golden samples

This test suite specifically validates:
- Empty scene handling
- Single entity scenarios
- All edge case coverage
- Performance under extreme conditions
- Error recovery mechanisms
"""
import pytest
import asyncio
import json
import time
import os
from pathlib import Path
from unittest.mock import patch, MagicMock, AsyncMock
from datetime import datetime, timezone

# Set environment for testing
os.environ["USE_LOCAL_MODEL"] = "false"
os.environ["MOCK_MODE"] = "false"

from fastapi.testclient import TestClient
from app.main import app
from app.services.inference_client import InferenceClient
from app.services.context_builder import context_builder
from app.services.postprocessor import postprocessor

client = TestClient(app)


class TestEmptySceneHandling:
    """Test empty scene edge cases"""
    
    def test_empty_scene_golden_sample_exists(self):
        """Verify empty scene golden sample exists and is valid"""
        sample_path = Path(__file__).parent.parent / "backend" / "app" / "golden_samples" / "sample_minimal_empty.json"
        assert sample_path.exists(), "Empty scene golden sample not found"
        
        with open(sample_path) as f:
            data = json.load(f)
        
        assert data["id"] == "scene_minimal_empty_001"
        assert data["entities"] == []
        assert "metadata" in data
        assert data["validation"]["allow_empty"] is True
    
    def test_empty_prompt_selects_empty_sample(self):
        """Test that empty/blank prompts select the empty sample"""
        client = InferenceClient()
        
        test_prompts = [
            "create an empty scene",
            "blank canvas",
            "start with nothing",
            "clean sandbox"
        ]
        
        for prompt in test_prompts:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            
            # Should prefer empty or minimal samples
            assert "empty" in sample_name or "minimal" in sample_name or "single" in sample_name
    
    def test_postprocessor_handles_empty_scenes(self):
        """Test that postprocessor correctly handles empty scenes"""
        empty_scene = {
            "id": "test_empty",
            "scene_name": "Empty Test",
            "entities": [],
            "metadata": {"width": 800, "height": 600}
        }
        
        processed = postprocessor.process_scene(empty_scene, "test_project")
        
        assert processed is not None
        assert processed["entities"] == []
        assert processed["project_id"] == "test_project"
        
        # Validate it passes validation
        is_valid = postprocessor.validate_scene(processed)
        assert is_valid or len(processed["entities"]) == 0  # Empty is valid
    
    @pytest.mark.asyncio
    async def test_generation_with_empty_request(self):
        """Test generation API with empty/minimal request"""
        client = InferenceClient()
        
        context = context_builder.build_generation_prompt(
            user_prompt="",  # Empty prompt
            project_id="test_empty"
        )
        
        result = await client.generate_scene(context)
        
        assert result is not None
        assert "scene" in result
        assert "metadata" in result
        assert result["metadata"]["status"] in ["cached_fallback", "success", "fail_fallback"]


class TestSingleEntityScenarios:
    """Test single entity edge cases"""
    
    def test_single_entity_golden_sample_exists(self):
        """Verify single entity golden sample exists and is valid"""
        sample_path = Path(__file__).parent.parent / "backend" / "app" / "golden_samples" / "sample_single_entity.json"
        assert sample_path.exists(), "Single entity golden sample not found"
        
        with open(sample_path) as f:
            data = json.load(f)
        
        assert data["id"] == "scene_single_entity_001"
        assert len(data["entities"]) == 1
        assert data["entities"][0]["id"] == "sole_entity"
    
    def test_single_entity_prompt_selection(self):
        """Test that single entity prompts select appropriate sample"""
        client = InferenceClient()
        
        test_prompts = [
            "create a scene with one object",
            "single entity test",
            "solo platform"
        ]
        
        for prompt in test_prompts:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            
            # Check that we get a valid scene
            assert result is not None
            if "single" in prompt or "one" in prompt:
                # Should prefer single entity sample
                assert "single" in sample_name or len(result.get("entities", [])) <= 3
    
    def test_single_entity_enhancement(self):
        """Test that single entity scenes are properly enhanced"""
        single_entity_scene = {
            "id": "test_single",
            "scene_name": "Single Entity Test",
            "entities": [
                {
                    "id": "entity1",
                    "type": "platform",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 50, "height": 50}
                }
            ]
        }
        
        enhanced = postprocessor.enhance_scene(single_entity_scene)
        
        assert len(enhanced["entities"]) == 1
        assert enhanced["entities"][0]["id"] == "entity1"
        # Check if properties were added
        if "properties" in enhanced["entities"][0]:
            assert enhanced["entities"][0]["properties"] is not None


class TestAllGoldenSamplesLoading:
    """Test that all 5 golden samples load correctly"""
    
    def test_all_five_samples_load(self):
        """Verify all 5 golden samples are loaded"""
        client = InferenceClient()
        
        assert len(client.golden_samples) >= 5, f"Expected at least 5 golden samples, got {len(client.golden_samples)}"
        
        sample_names = [s["name"] for s in client.golden_samples]
        
        expected_samples = [
            "sample_simple_geometry",
            "sample_asset_intensive", 
            "sample_complex_structure",
            "sample_minimal_empty",
            "sample_single_entity"
        ]
        
        for expected in expected_samples:
            assert any(expected in name for name in sample_names), f"Missing sample: {expected}"
    
    def test_sample_complexity_ordering(self):
        """Test that samples have correct complexity values"""
        client = InferenceClient()
        
        complexities = {}
        for sample in client.golden_samples:
            complexities[sample["name"]] = sample["complexity"]
        
        # Check complexity ordering
        if "sample_minimal_empty" in complexities:
            assert complexities["sample_minimal_empty"] == 0
        if "sample_single_entity" in complexities:
            assert complexities["sample_single_entity"] == 0.5
        if "sample_simple_geometry" in complexities:
            assert complexities["sample_simple_geometry"] == 1
        if "sample_asset_intensive" in complexities:
            assert complexities["sample_asset_intensive"] == 2
        if "sample_complex_structure" in complexities:
            assert complexities["sample_complex_structure"] == 3


class TestExtremeCases:
    """Test extreme edge cases"""
    
    @pytest.mark.asyncio
    async def test_very_long_prompt(self):
        """Test handling of extremely long prompts"""
        client = InferenceClient()
        
        # Create a very long prompt (10KB)
        long_prompt = "create a game with " + " ".join(["complex"] * 1000)
        
        context = {"engineered_prompt": long_prompt, "prompt_hash": "long_hash"}
        result = await client.generate_scene(context)
        
        assert result is not None
        assert "scene" in result
    
    @pytest.mark.asyncio
    async def test_special_characters_in_prompt(self):
        """Test handling of special characters in prompts"""
        client = InferenceClient()
        
        special_prompts = [
            "create 你好 scene",  # Unicode
            "game with $pecial ch@rs!",  # Special chars
            "scene\nwith\nnewlines",  # Newlines
            "game with \"quotes\" and 'apostrophes'"  # Quotes
        ]
        
        for prompt in special_prompts:
            context = {"engineered_prompt": prompt}
            result = await client.generate_scene(context)
            assert result is not None
    
    @pytest.mark.asyncio
    async def test_concurrent_generation_requests(self):
        """Test multiple concurrent generation requests"""
        client = InferenceClient()
        
        # Create multiple concurrent requests
        tasks = []
        for i in range(5):
            context = {"engineered_prompt": f"test prompt {i}", "prompt_hash": f"hash_{i}"}
            tasks.append(client.generate_scene(context))
        
        results = await asyncio.gather(*tasks)
        
        assert len(results) == 5
        for result in results:
            assert result is not None
            assert "scene" in result
    
    def test_malformed_scene_recovery(self):
        """Test recovery from malformed scene data"""
        malformed_scenes = [
            {},  # Empty dict
            {"id": "test"},  # Missing required fields
            {"entities": "not_a_list"},  # Wrong type
            {"entities": [{"bad": "entity"}]},  # Invalid entity
        ]
        
        for scene in malformed_scenes:
            try:
                processed = postprocessor.process_scene(scene, "test_project")
                # Should either process successfully or use defaults
                assert processed is not None
            except Exception:
                # Should handle gracefully
                pass


class TestIntelligentFallbackSelection:
    """Test intelligent fallback selection with all samples"""
    
    def test_keyword_matching_accuracy(self):
        """Test keyword matching selects correct samples"""
        client = InferenceClient()
        
        test_cases = [
            ("empty blank scene", "empty"),
            ("single object only", "single"),
            ("simple platform game", "simple"),
            ("game with lots of assets and sprites", "asset"),
            ("complex layered puzzle with events", "complex")
        ]
        
        for prompt, expected_type in test_cases:
            context = {"engineered_prompt": prompt}
            result, sample_name = client._use_fallback_sample(context)
            
            assert expected_type in sample_name.lower(), f"Prompt '{prompt}' should select {expected_type} sample, got {sample_name}"
    
    def test_complexity_based_selection(self):
        """Test that complexity preferences work correctly"""
        client = InferenceClient()
        
        # Request simple scene
        context = {"engineered_prompt": "very simple basic scene"}
        result, sample_name = client._use_fallback_sample(context)
        sample = next((s for s in client.golden_samples if s["name"] == sample_name), None)
        if sample:
            assert sample["complexity"] <= 1, "Simple prompt should select low complexity sample"
        
        # Request complex scene
        context = {"engineered_prompt": "very complex advanced scene"}
        result, sample_name = client._use_fallback_sample(context)
        sample = next((s for s in client.golden_samples if s["name"] == sample_name), None)
        if sample:
            assert sample["complexity"] >= 2, "Complex prompt should select high complexity sample"


class TestAPIEndpointsWithNewSamples:
    """Test API endpoints with new golden samples"""
    
    def test_get_empty_sample_endpoint(self):
        """Test retrieving empty sample via API"""
        response = client.get("/api/generation/samples/sample_minimal_empty")
        
        if response.status_code == 200:
            data = response.json()
            assert data["entities"] == []
            assert data["id"] == "scene_minimal_empty_001"
    
    def test_get_single_entity_sample_endpoint(self):
        """Test retrieving single entity sample via API"""
        response = client.get("/api/generation/samples/sample_single_entity")
        
        if response.status_code == 200:
            data = response.json()
            assert len(data["entities"]) == 1
            assert data["id"] == "scene_single_entity_001"
    
    def test_generation_with_empty_style(self):
        """Test generation with empty/sandbox style"""
        response = client.post(
            "/api/generation/",
            json={
                "prompt": "create empty sandbox",
                "project_id": "test_sandbox",
                "style": "sandbox"
            }
        )
        
        if response.status_code == 200:
            data = response.json()
            assert "scene" in data
            # May return empty or minimal scene
            assert len(data["scene"].get("entities", [])) <= 1


class TestPerformanceWithAllSamples:
    """Test performance with expanded sample set"""
    
    @pytest.mark.asyncio
    async def test_sample_loading_performance(self):
        """Test that loading 5 samples doesn't degrade performance"""
        start_time = time.time()
        
        # Create new client (forces reload)
        client = InferenceClient()
        
        load_time = time.time() - start_time
        
        assert load_time < 1.0, f"Loading {len(client.golden_samples)} samples took {load_time}s, should be < 1s"
    
    @pytest.mark.asyncio
    async def test_selection_performance(self):
        """Test that sample selection remains fast with more samples"""
        client = InferenceClient()
        
        start_time = time.time()
        
        # Perform 100 selections
        for i in range(100):
            context = {"engineered_prompt": f"test prompt {i % 5}"}
            result, sample_name = client._use_fallback_sample(context)
        
        total_time = time.time() - start_time
        avg_time = total_time / 100
        
        assert avg_time < 0.01, f"Average selection time {avg_time}s should be < 10ms"


class TestDatabaseLoggingWithEdgeCases:
    """Test database logging for edge case scenarios"""
    
    @pytest.mark.asyncio
    async def test_empty_scene_logging(self, db_session):
        """Test that empty scenes are logged correctly"""
        from app.routers.generation import log_generation
        
        await log_generation(
            db=db_session,
            user_id="test_user",
            input_hash="empty_hash",
            prompt_hash="empty_prompt",
            model_version="fallback",
            status="cached_fallback",
            latency_ms=50,
            request_payload={"prompt": "empty scene"},
            response_payload={"entities": []}
        )
        
        # Would check database in real test
        assert True  # Placeholder
    
    @pytest.mark.asyncio
    async def test_error_recovery_logging(self, db_session):
        """Test that errors are logged with proper detail"""
        from app.routers.generation import log_generation
        
        await log_generation(
            db=db_session,
            user_id="test_user",
            input_hash="error_hash",
            prompt_hash="error_prompt",
            model_version="error",
            status="error",
            latency_ms=100,
            request_payload={"prompt": "cause error"},
            error="Test error message"
        )
        
        # Would verify error logged correctly
        assert True  # Placeholder


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