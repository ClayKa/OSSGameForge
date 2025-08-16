# Testing Documentation

## Overview

This document provides comprehensive guidance on testing strategies, golden sample management, and quality assurance procedures for the OSSGameForge project.

## Table of Contents
1. [Golden Samples](#golden-samples)
2. [How to Add New Golden Sample Tests](#how-to-add-new-golden-sample-tests)
3. [Testing Strategy](#testing-strategy)
4. [CI/CD Pipeline](#cicd-pipeline)
5. [Performance Testing](#performance-testing)

## Golden Samples

Golden samples are pre-defined, version-controlled JSON files that serve as:
- **Fallback mechanisms** when the AI model is unavailable
- **Baseline references** for quality testing
- **Regression test data** to ensure consistent output
- **Performance benchmarks** for rendering and parsing

### Current Golden Samples

We maintain five comprehensive golden samples in `backend/app/golden_samples/` achieving **100% edge case coverage**:

1. **sample_simple_geometry.json**
   - **Purpose**: Tests core rendering logic with basic geometric shapes
   - **Complexity**: Low (1/3)
   - **Coverage**: Basic platforms, player movement, collectibles, collision layers
   - **Keywords**: simple, basic, geometry, platform, block

2. **sample_asset_intensive.json**
   - **Purpose**: Tests asset loading, resource management, and sprite rendering
   - **Complexity**: Medium (2/3)
   - **Coverage**: Images, audio, spritesheets, tiled platforms
   - **Keywords**: asset, texture, sprite, image, audio, forest

3. **sample_complex_structure.json**
   - **Purpose**: Tests complex JSON parsing, nested structures, and advanced features
   - **Complexity**: High (3/3)
   - **Coverage**: Layers, events, triggers, particle systems, scripts, UI elements
   - **Keywords**: complex, advanced, layer, nested, puzzle, mechanism

4. **sample_minimal_empty.json**
   - **Purpose**: Tests edge case handling for empty scenes
   - **Complexity**: Minimal (0/3)
   - **Coverage**: Empty entities array, sandbox initialization, fallback behavior
   - **Keywords**: empty, blank, none, minimal, sandbox, clean, start

5. **sample_single_entity.json**
   - **Purpose**: Tests minimal viable scene with single entity
   - **Complexity**: Minimal (0.5/3)
   - **Coverage**: Single entity rendering, minimal scene validation
   - **Keywords**: single, one, solo, minimal, basic, simple

### Edge Case Coverage

Our golden samples provide **100% coverage** of critical edge cases:
- ✅ Empty entities (sample_minimal_empty.json)
- ✅ Single entity (sample_single_entity.json)
- ✅ Large entity count (10+ entities)
- ✅ Nested structures (entity groups with children)
- ✅ Multiple layers (4 rendering layers)
- ✅ Events and triggers (3 event types)
- ✅ Various entity types (6+ different types)
- ✅ Asset references (9 different assets)
- ✅ Collision layers (physics configuration)
- ✅ Particle systems (environmental effects)
- ✅ UI elements (HUD and overlays)

## How to Add New Golden Sample Tests

Our testing framework automatically discovers and incorporates new golden samples. Follow these steps to add a new test case:

### Step 1: Define the Scenario

Identify what specific feature or edge case you want to test. Examples:
- New entity types (e.g., moving platforms, destructible blocks)
- Specific asset combinations (e.g., parallax backgrounds)
- Complex game mechanics (e.g., physics simulations, AI behaviors)
- Performance edge cases (e.g., 1000+ entities)

### Step 2: Create the Sample File

1. Navigate to `backend/app/golden_samples/`
2. Create a new JSON file with a descriptive name following the pattern: `sample_[description].json`
   ```
   sample_moving_platforms.json
   sample_particle_effects.json
   sample_multiplayer_scene.json
   ```

3. Structure your JSON according to the scene schema:
   ```json
   {
     "id": "scene_[unique_id]",
     "scene_name": "Descriptive Name",
     "description": "What this sample tests",
     "style": "platformer|rpg|puzzle|adventure",
     "metadata": {
       "width": 1920,
       "height": 1080,
       "complexity_score": 1-100
     },
     "entities": [
       // Your test entities here
     ]
   }
   ```

### Step 3: Add Metadata for Intelligent Selection

Update `backend/app/services/inference_client.py` to include metadata for your sample:

```python
sample_metadata = {
    "sample_your_new_test.json": {
        "keywords": ["keyword1", "keyword2", "keyword3"],
        "complexity": 1-3,  # 1=simple, 2=medium, 3=complex
        "description": "Brief description of what this tests"
    }
}
```

### Step 4: Validate the Schema

Ensure your JSON validates against our Pydantic models:

```bash
python -c "
import json
from backend.app.schemas.generation import SceneSchema
with open('backend/app/golden_samples/sample_your_new_test.json') as f:
    data = json.load(f)
    SceneSchema(**data)  # Will raise if invalid
print('✓ Schema valid')
"
```

### Step 5: Write Specific Tests (Optional)

For complex scenarios, add specific test cases:

```python
# tests/test_golden_sample_your_feature.py
import pytest
from backend.app.services.inference_client import inference_client

def test_your_new_golden_sample():
    sample = inference_client.load_golden_sample("sample_your_new_test")
    assert sample is not None
    assert "expected_feature" in sample
    # Add specific assertions for your test case
```

### Step 6: Update CI Configuration

The CI pipeline automatically discovers new samples, but for specific test suites:

1. Add to `.github/workflows/ci.yml` if needed:
   ```yaml
   - name: Test New Golden Sample
     run: pytest tests/test_golden_sample_your_feature.py -v
   ```

## Testing Strategy

### Unit Tests
- **Location**: `tests/backend/unit/`
- **Coverage Target**: >80%
- **Run**: `pytest tests/backend/unit/ --cov=backend.app`

### Integration Tests
- **Location**: `tests/backend/integration/`
- **Focus**: Service interactions, database operations
- **Run**: `pytest tests/backend/integration/`

### End-to-End Tests
- **Location**: `tests/e2e/`
- **Tool**: Playwright
- **Focus**: Complete user workflows, HTML5 export validation
- **Run**: `npm run test:e2e`

### Golden Sample Tests
- **Location**: `tests/test_generation_pipeline.py`
- **Focus**: Scene generation, fallback mechanisms
- **Run**: `USE_LOCAL_MODEL=false pytest tests/test_generation_pipeline.py`

## CI/CD Pipeline

### Fast Tests (Every PR)
- **Duration**: 1-2 minutes
- **Includes**:
  - Linting (`ruff check`)
  - Unit tests
  - Schema validation
  - Golden sample loading

### Comprehensive Tests (On Merge)
- **Duration**: 2-5 minutes
- **Includes**:
  - All fast tests
  - Integration tests
  - E2E browser tests
  - Visual regression tests
  - Performance benchmarks

### Test Execution Order
1. **Pre-commit hooks**: Format check, basic linting
2. **CI Fast Lane**: Critical path tests
3. **CI Full Suite**: Complete validation
4. **Post-merge**: Deploy to staging, smoke tests

## Performance Testing

### Latency Expectations

| Mode | Expected Latency | Hardware Requirements |
|------|-----------------|----------------------|
| Fallback Mode | < 100ms | None |
| Local Model (CPU) | 30-60s | 8+ CPU cores |
| Local Model (GPU) | 15-45s | 16GB+ VRAM |
| Mock Mode | 500-1500ms | None |

### Load Testing

Test the system under various loads:

```bash
# Generate 100 concurrent requests
python tests/performance/load_test.py --concurrent 100 --duration 60
```

### Memory Profiling

Monitor memory usage during golden sample processing:

```bash
python -m memory_profiler tests/performance/memory_test.py
```

## Debugging Failed Tests

### Common Issues and Solutions

1. **Golden Sample Not Found**
   - Check file exists in `backend/app/golden_samples/`
   - Verify file name matches pattern `sample_*.json`
   - Check file permissions

2. **Schema Validation Errors**
   - Validate JSON syntax
   - Check required fields are present
   - Verify data types match schema

3. **Inference Client Failures**
   - Check `USE_LOCAL_MODEL` environment variable
   - Verify golden samples are loaded (`/generate/status` endpoint)
   - Check logs for fallback reasons

4. **CI Pipeline Timeouts**
   - Split long-running tests into separate jobs
   - Use test parallelization
   - Cache dependencies

## Best Practices

1. **Always test with golden samples first** before attempting model inference
2. **Create focused samples** that test one specific feature
3. **Document sample purpose** in the description field
4. **Keep samples version-controlled** for regression testing
5. **Monitor sample performance** to catch rendering slowdowns
6. **Use deterministic IDs** in tests for consistent assertions

## Troubleshooting

### Enable Debug Logging

```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

### Check Golden Sample Loading

```bash
curl http://localhost:8000/generate/samples
```

### Verify Fallback Mechanism

```bash
USE_LOCAL_MODEL=false curl -X POST http://localhost:8000/generate \
  -H "Content-Type: application/json" \
  -d '{"prompt": "simple platform game", "project_id": "test"}'
```

## Contact

For questions about testing strategies or golden samples, please refer to:
- GitHub Issues: https://github.com/ClayKa/oss-game-forge/issues
- Documentation: `/docs/`
- Team Lead: Check CODEOWNERS file