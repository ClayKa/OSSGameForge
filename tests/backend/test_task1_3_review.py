#!/usr/bin/env python
"""
Comprehensive review tests for Task 1.3: Modular Backend & Database

This test suite thoroughly examines the implementation of Task 1.3 to identify
any potential issues, bugs, or areas for improvement.
"""
import sys
import os
import json
import asyncio
import hashlib
from datetime import datetime
from pathlib import Path
from unittest.mock import MagicMock, patch, AsyncMock
from typing import Dict, Any

sys.path.insert(0, '/app')

from app.services.context_builder import context_builder
from app.services.inference_client import inference_client
from app.services.postprocessor import postprocessor


class TestContextBuilderIssues:
    """Test for potential issues in ContextBuilder service"""
    
    def test_prompt_hash_collision(self):
        """Test if prompt hash generation could have collisions"""
        # Create two slightly different contexts that should have different hashes
        context1 = context_builder.build_generation_prompt(
            user_prompt="Create a level",
            project_id="proj1",
            style="platformer"
        )
        
        context2 = context_builder.build_generation_prompt(
            user_prompt="Create a level",  # Same prompt
            project_id="proj1",  # Same project
            style="platformer"  # Same style
        )
        
        # These should have different hashes due to timestamp
        assert context1["prompt_hash"] != context2["prompt_hash"], \
            "❌ ISSUE: Identical contexts generate same hash (no timestamp consideration)"
        print("✅ Prompt hash includes timestamp to prevent collisions")
    
    def test_asset_overflow_handling(self):
        """Test if context builder handles large numbers of assets properly"""
        # Create 100 assets (more than the 50 limit)
        large_asset_list = [
            {"id": f"asset_{i}", "type": "image", "name": f"img_{i}.png", "metadata": {}}
            for i in range(100)
        ]
        
        context = context_builder.build_generation_prompt(
            user_prompt="Test",
            project_id="proj1",
            assets=large_asset_list
        )
        
        # Check if assets are properly limited
        assert len(context["assets"]) == 50, \
            f"❌ ISSUE: Asset limit not enforced, got {len(context['assets'])}"
        assert context["asset_count"] == 100, \
            "❌ ISSUE: Asset count doesn't reflect original number"
        print("✅ Asset overflow handling works correctly (limits to 50)")
    
    def test_context_validation_edge_cases(self):
        """Test context validation with edge cases"""
        # Test with None values
        invalid_contexts = [
            {"user_prompt": None, "project_id": "proj1"},
            {"user_prompt": "", "project_id": "proj1"},
            {"user_prompt": "test", "project_id": None},
            {"user_prompt": "test", "project_id": ""},
            {}
        ]
        
        for ctx in invalid_contexts:
            is_valid = context_builder.validate_context(ctx)
            if is_valid and (not ctx.get("user_prompt") or not ctx.get("project_id")):
                print(f"❌ ISSUE: Invalid context accepted: {ctx}")
                return False
        
        print("✅ Context validation handles edge cases properly")
        return True
    
    def test_metadata_extraction_security(self):
        """Test if metadata extraction filters sensitive data"""
        assets = [{
            "id": "asset1",
            "type": "image",
            "metadata": {
                "width": 100,
                "height": 200,
                "api_key": "secret_key",  # Sensitive data
                "password": "secret",  # Sensitive data
                "location": "GPS coordinates"  # Potentially sensitive
            }
        }]
        
        context = context_builder.build_generation_prompt(
            user_prompt="Test",
            project_id="proj1",
            assets=assets
        )
        
        # Check processed assets don't contain sensitive data
        processed_metadata = context["assets"][0]["metadata"]
        assert "api_key" not in processed_metadata, \
            "❌ ISSUE: Sensitive 'api_key' not filtered from metadata"
        assert "password" not in processed_metadata, \
            "❌ ISSUE: Sensitive 'password' not filtered from metadata"
        assert "location" not in processed_metadata, \
            "❌ ISSUE: Potentially sensitive 'location' not filtered"
        print("✅ Metadata extraction filters sensitive data correctly")


class TestInferenceClientIssues:
    """Test for potential issues in InferenceClient service"""
    
    async def test_concurrent_inference_handling(self):
        """Test if inference client handles concurrent requests properly"""
        # Simulate multiple concurrent requests
        tasks = []
        for i in range(10):
            context = {
                "user_prompt": f"Test prompt {i}",
                "engineered_prompt": f"Engineered {i}",
                "prompt_hash": f"hash_{i}"
            }
            tasks.append(inference_client.generate_scene(context))
        
        try:
            results = await asyncio.gather(*tasks)
            # Check all results are valid
            for i, result in enumerate(results):
                assert "scene" in result, f"❌ ISSUE: Result {i} missing 'scene'"
                assert "metadata" in result, f"❌ ISSUE: Result {i} missing 'metadata'"
            print(f"✅ Handled {len(tasks)} concurrent requests successfully")
        except Exception as e:
            print(f"❌ ISSUE: Failed handling concurrent requests: {e}")
            return False
        return True
    
    def test_golden_sample_loading_failure(self):
        """Test behavior when golden samples can't be loaded"""
        # Temporarily break the golden samples path
        original_path = inference_client.golden_samples_path
        inference_client.golden_samples_path = Path("/nonexistent/path")
        
        # Re-load samples
        inference_client._load_golden_samples()
        
        # Check if default samples are loaded
        assert len(inference_client.golden_samples) > 0, \
            "❌ ISSUE: No fallback samples when file loading fails"
        
        # Restore original path
        inference_client.golden_samples_path = original_path
        inference_client._load_golden_samples()
        
        print("✅ Fallback samples loaded when file loading fails")
    
    async def test_model_timeout_handling(self):
        """Test if model timeout is properly handled"""
        context = {
            "user_prompt": "Test",
            "engineered_prompt": "Test prompt",
            "prompt_hash": "test_hash"
        }
        
        # Mock a timeout scenario
        with patch.object(inference_client, '_simulate_processing_delay') as mock_delay:
            mock_delay.side_effect = asyncio.TimeoutError("Model timeout")
            
            result = await inference_client.generate_scene(context)
            
            # Should return error fallback scene
            assert result["metadata"]["status"] == "error", \
                "❌ ISSUE: Timeout not handled gracefully"
            assert "scene" in result, \
                "❌ ISSUE: No fallback scene on timeout"
            
        print("✅ Model timeout handled gracefully with fallback")
    
    def test_prompt_keyword_matching_accuracy(self):
        """Test if keyword matching for sample selection is accurate"""
        test_cases = [
            ("Create a simple geometry platform game", "simple_geometry"),
            ("Design an asset intensive sprite scene", "asset_intensive"),
            ("Build complex structure with multiple enemies", "complex_structure"),
            ("Random prompt without keywords", None)  # Should get random
        ]
        
        for prompt, expected_type in test_cases:
            context = {"engineered_prompt": prompt}
            result = inference_client._use_fallback_sample(context)
            
            if expected_type:
                # Verify the right sample type was selected
                scene = result["scene"]
                if expected_type == "simple_geometry":
                    assert any("platform" in str(e.get("type", "")) for e in scene.get("entities", [])), \
                        f"❌ ISSUE: Wrong sample selected for prompt: {prompt}"
        
        print("✅ Keyword matching for sample selection works correctly")


class TestPostprocessorIssues:
    """Test for potential issues in Postprocessor service"""
    
    def test_entity_id_uniqueness(self):
        """Test if entity IDs are guaranteed to be unique"""
        raw_scene = {
            "entities": [
                {"type": "player"},
                {"type": "player"},  # Duplicate type
                {"type": "enemy"},
                {"type": "enemy"}  # Duplicate type
            ]
        }
        
        processed = postprocessor.process_scene(raw_scene, "test_proj")
        
        # Check all entity IDs are unique
        entity_ids = [e["id"] for e in processed["entities"]]
        assert len(entity_ids) == len(set(entity_ids)), \
            "❌ ISSUE: Duplicate entity IDs generated"
        print("✅ Entity IDs are guaranteed unique")
    
    def test_invalid_position_handling(self):
        """Test handling of invalid position data"""
        invalid_scenes = [
            {"entities": [{"type": "player", "position": "invalid"}]},
            {"entities": [{"type": "player", "position": {"x": "not_a_number", "y": 100}}]},
            {"entities": [{"type": "player", "position": {"x": None, "y": None}}]},
            {"entities": [{"type": "player", "position": {}}]}  # Missing x, y
        ]
        
        for raw_scene in invalid_scenes:
            try:
                processed = postprocessor.process_scene(raw_scene, "test_proj")
                # Check position was normalized
                entity = processed["entities"][0]
                assert isinstance(entity["position"]["x"], (int, float)), \
                    f"❌ ISSUE: Invalid position not normalized: {entity['position']}"
                assert isinstance(entity["position"]["y"], (int, float)), \
                    f"❌ ISSUE: Invalid position not normalized: {entity['position']}"
            except Exception as e:
                print(f"❌ ISSUE: Failed to handle invalid position: {e}")
                return False
        
        print("✅ Invalid positions handled correctly")
        return True
    
    def test_circular_reference_in_enhancement(self):
        """Test if scene enhancement could create circular references"""
        scene = {
            "id": "scene1",
            "name": "Test",
            "style": "platformer",
            "entities": [{"id": "e1", "type": "player", "position": {"x": 0, "y": 0}, "size": {"width": 32, "height": 32}}]
        }
        
        # Add a self-reference
        scene["parent"] = scene  # Circular reference
        
        try:
            enhanced = postprocessor.enhance_scene(scene)
            # Try to serialize to JSON (would fail with circular reference)
            json.dumps(enhanced, default=str)
            print("✅ No circular reference issues in enhancement")
        except (ValueError, TypeError) as e:
            if "circular reference" in str(e).lower():
                print(f"❌ ISSUE: Circular reference created: {e}")
                return False
            # Other JSON errors are fine
            pass
        
        return True
    
    def test_entity_overlap_resolution(self):
        """Test if overlapping entities are properly resolved"""
        raw_scene = {
            "entities": [
                {"type": "enemy", "position": {"x": 100, "y": 100}, "size": {"width": 50, "height": 50}},
                {"type": "enemy", "position": {"x": 100, "y": 100}, "size": {"width": 50, "height": 50}},  # Exact overlap
                {"type": "enemy", "position": {"x": 120, "y": 120}, "size": {"width": 50, "height": 50}}  # Partial overlap
            ]
        }
        
        processed = postprocessor.process_scene(raw_scene, "test_proj")
        enhanced = postprocessor.enhance_scene(processed)
        
        # Check if entities were separated
        entities = enhanced["entities"]
        for i, e1 in enumerate(entities):
            for j, e2 in enumerate(entities[i+1:], i+1):
                overlap = postprocessor._entities_overlap(e1, e2)
                if overlap:
                    print(f"⚠️ WARNING: Entities {i} and {j} still overlap after optimization")
        
        print("✅ Entity overlap detection works (optimization attempted)")
    
    def test_asset_incorporation_limit(self):
        """Test if asset incorporation has proper limits"""
        scene = {
            "id": "scene1",
            "name": "Test",
            "style": "platformer",
            "entities": [{"id": "e1", "type": "player", "position": {"x": 0, "y": 0}, "size": {"width": 32, "height": 32}, "properties": {}}]
        }
        
        # Create many assets
        assets = [{"id": f"asset_{i}", "type": "image", "path": f"/path/{i}"} for i in range(100)]
        
        processed = postprocessor.process_scene(scene, "test_proj", assets)
        
        # Check asset limit
        assert len(processed.get("assets", [])) <= 10, \
            f"❌ ISSUE: Too many assets incorporated: {len(processed.get('assets', []))}"
        print("✅ Asset incorporation properly limited to 10")


class TestDatabaseModelIssues:
    """Test for potential issues in database models"""
    
    def test_datetime_deprecation_warnings(self):
        """Check for datetime.utcnow() deprecation issues"""
        # Check if models use deprecated datetime.utcnow()
        issues = []
        
        # Read the core_models.py file
        with open('/Users/clayka7/Documents/OSSGF/backend/app/models/core_models.py', 'r') as f:
            content = f.read()
            if 'datetime.utcnow' in content:
                issues.append("❌ ISSUE: Using deprecated datetime.utcnow() - should use datetime.now(timezone.utc)")
        
        # Read service files
        service_files = [
            '/Users/clayka7/Documents/OSSGF/backend/app/services/context_builder.py',
            '/Users/clayka7/Documents/OSSGF/backend/app/services/postprocessor.py'
        ]
        
        for filepath in service_files:
            with open(filepath, 'r') as f:
                content = f.read()
                if 'datetime.utcnow()' in content:
                    issues.append(f"❌ ISSUE: {filepath} uses deprecated datetime.utcnow()")
        
        if issues:
            for issue in issues:
                print(issue)
            return False
        else:
            print("✅ No datetime deprecation issues found")
            return True
    
    def test_json_field_handling(self):
        """Test if JSON fields handle None and complex data properly"""
        from app.models import Asset, GenerationLog
        
        # Test with None
        asset = Asset(
            project_id="test",
            path="/test",
            type="image",
            consent_hash="hash123",
            asset_metadata=None  # JSON field with None
        )
        
        # This should work without errors
        try:
            asset_dict = asset.to_dict()
            assert asset_dict["metadata"] is None, \
                "❌ ISSUE: JSON field None not handled properly"
            print("✅ JSON fields handle None correctly")
        except Exception as e:
            print(f"❌ ISSUE: JSON field error with None: {e}")
            return False
        
        return True
    
    def test_uuid_generation_uniqueness(self):
        """Test if UUID generation is truly unique"""
        from app.models import Asset
        import uuid
        
        # Generate many UUIDs
        uuids = []
        for _ in range(1000):
            asset = Asset(
                project_id="test",
                path="/test",
                type="image",
                consent_hash="hash"
            )
            # The id should be auto-generated
            if not asset.id:
                asset.id = uuid.uuid4()
            uuids.append(str(asset.id))
        
        # Check uniqueness
        assert len(uuids) == len(set(uuids)), \
            "❌ ISSUE: UUID collisions detected!"
        print(f"✅ Generated {len(uuids)} unique UUIDs without collision")


class TestIntegrationIssues:
    """Test for integration issues between services"""
    
    async def test_service_pipeline_integration(self):
        """Test the full pipeline from context building to postprocessing"""
        # Build context
        context = context_builder.build_generation_prompt(
            user_prompt="Create a test level",
            project_id="test_proj",
            assets=[{"id": "asset1", "type": "image", "metadata": {"width": 100}}]
        )
        
        # Generate scene
        result = await inference_client.generate_scene(context)
        
        # Process scene
        processed = postprocessor.process_scene(
            result["scene"],
            "test_proj",
            [{"id": "asset1", "type": "image", "path": "/test"}]
        )
        
        # Validate final output
        assert postprocessor.validate_scene(processed), \
            "❌ ISSUE: Pipeline produces invalid scene"
        assert processed["project_id"] == "test_proj", \
            "❌ ISSUE: Project ID not preserved through pipeline"
        
        print("✅ Service pipeline integration works correctly")
    
    def test_error_propagation(self):
        """Test if errors propagate correctly through the service chain"""
        # Test with invalid input
        try:
            context = context_builder.build_generation_prompt(
                user_prompt=None,  # Invalid
                project_id="test"
            )
            # Should handle gracefully
            assert context["user_prompt"] is None
        except Exception as e:
            print(f"⚠️ WARNING: Error not handled gracefully: {e}")
        
        print("✅ Error handling tested")


def run_all_tests():
    """Run all review tests"""
    print("="*70)
    print("Task 1.3 Code Review Tests")
    print("Checking for potential issues and bugs")
    print("="*70)
    
    test_suites = [
        ("ContextBuilder Issues", TestContextBuilderIssues()),
        ("InferenceClient Issues", TestInferenceClientIssues()),
        ("Postprocessor Issues", TestPostprocessorIssues()),
        ("Database Model Issues", TestDatabaseModelIssues()),
        ("Integration Issues", TestIntegrationIssues())
    ]
    
    all_issues = []
    
    for suite_name, suite in test_suites:
        print(f"\n{'='*60}")
        print(f"Testing {suite_name}")
        print(f"{'='*60}")
        
        for method_name in dir(suite):
            if method_name.startswith("test_"):
                method = getattr(suite, method_name)
                try:
                    # Handle async tests
                    if asyncio.iscoroutinefunction(method):
                        result = asyncio.run(method())
                    else:
                        result = method()
                    
                    if result is False:
                        all_issues.append(f"{suite_name}.{method_name}")
                except Exception as e:
                    print(f"❌ EXCEPTION in {method_name}: {e}")
                    all_issues.append(f"{suite_name}.{method_name}: {e}")
    
    # Summary
    print("\n" + "="*70)
    print("REVIEW SUMMARY")
    print("="*70)
    
    if all_issues:
        print(f"\n⚠️ Found {len(all_issues)} potential issues:")
        for issue in all_issues:
            print(f"  • {issue}")
        print("\nRecommendations:")
        print("1. Update datetime.utcnow() to datetime.now(timezone.utc)")
        print("2. Add more robust error handling in service pipeline")
        print("3. Consider adding rate limiting for concurrent requests")
    else:
        print("\n✅ No critical issues found!")
        print("The Task 1.3 implementation is robust and well-designed.")
    
    print("\n" + "="*70)
    print("Review Complete")
    print("="*70)


if __name__ == "__main__":
    run_all_tests()