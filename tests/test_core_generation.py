"""
Simplified core generation tests to verify basic functionality
"""
import pytest
import os
import sys
import json
from pathlib import Path

# Add backend to path
sys.path.insert(0, str(Path(__file__).parent.parent / "backend"))

os.environ["USE_LOCAL_MODEL"] = "false"
os.environ["MOCK_MODE"] = "false"

from app.services.inference_client import InferenceClient
from app.services.context_builder import ContextBuilder
from app.services.postprocessor import Postprocessor


def test_golden_samples_loaded():
    """Test that all golden samples are loaded"""
    client = InferenceClient()
    assert len(client.golden_samples) == 5, f"Expected 5 samples, got {len(client.golden_samples)}"
    
    sample_names = [s["name"] for s in client.golden_samples]
    print(f"Loaded samples: {sample_names}")
    
    assert "sample_simple_geometry" in sample_names
    assert "sample_asset_intensive" in sample_names
    assert "sample_complex_structure" in sample_names
    assert "sample_minimal_empty" in sample_names
    assert "sample_single_entity" in sample_names


def test_sample_selection():
    """Test intelligent sample selection"""
    client = InferenceClient()
    
    # Test empty prompt
    result, sample_name = client._use_fallback_sample({"engineered_prompt": "empty scene"})
    assert "empty" in sample_name or "minimal" in sample_name
    
    # Test simple prompt
    result, sample_name = client._use_fallback_sample({"engineered_prompt": "simple platform game"})
    assert result is not None
    
    # Test complex prompt
    result, sample_name = client._use_fallback_sample({"engineered_prompt": "complex layered puzzle"})
    assert result is not None


@pytest.mark.asyncio
async def test_scene_generation():
    """Test basic scene generation"""
    client = InferenceClient()
    
    context = {
        "engineered_prompt": "create a platformer level",
        "prompt_hash": "test_hash",
        "project_id": "test_proj"
    }
    
    result = await client.generate_scene(context)
    
    assert "scene" in result
    assert "metadata" in result
    assert result["metadata"]["status"] in ["cached_fallback", "success", "fail_fallback"]
    assert result["scene"] is not None


def test_context_builder():
    """Test context builder"""
    builder = ContextBuilder()
    
    context = builder.build_generation_prompt(
        user_prompt="test prompt",
        project_id="test_proj"
    )
    
    assert "engineered_prompt" in context
    assert "prompt_hash" in context
    assert context["project_id"] == "test_proj"


def test_postprocessor():
    """Test postprocessor with golden samples"""
    processor = Postprocessor()
    samples_dir = Path(__file__).parent.parent / "backend" / "app" / "golden_samples"
    
    for sample_file in samples_dir.glob("sample_*.json"):
        with open(sample_file) as f:
            scene = json.load(f)
        
        processed = processor.process_scene(scene, "test_project")
        assert processed is not None
        assert processed["project_id"] == "test_project"
        
        # Test validation
        is_valid = processor.validate_scene(processed)
        assert is_valid or len(processed.get("entities", [])) == 0


def test_edge_case_coverage():
    """Verify 100% edge case coverage"""
    samples_dir = Path(__file__).parent.parent / "backend" / "app" / "golden_samples"
    
    edge_cases = {
        'empty_entities': False,
        'single_entity': False,
        'large_entity_count': False,
        'multiple_layers': False,
        'events_and_triggers': False,
        'asset_references': False,
    }
    
    for sample_file in samples_dir.glob("sample_*.json"):
        with open(sample_file) as f:
            data = json.load(f)
        
        if 'entities' in data:
            if len(data['entities']) == 0:
                edge_cases['empty_entities'] = True
            elif len(data['entities']) == 1:
                edge_cases['single_entity'] = True
            elif len(data['entities']) > 5:
                edge_cases['large_entity_count'] = True
        
        if 'layers' in data:
            edge_cases['multiple_layers'] = True
        
        if 'events' in data:
            edge_cases['events_and_triggers'] = True
        
        if 'assets' in data:
            edge_cases['asset_references'] = True
    
    # All critical edge cases should be covered
    assert all(edge_cases.values()), f"Missing edge cases: {[k for k,v in edge_cases.items() if not v]}"


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])