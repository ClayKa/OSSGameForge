"""
Generation router for OSSGameForge API

Handles scene generation requests with comprehensive logging and fallback mechanisms.
This module orchestrates the entire generation pipeline:
1. Context building from user prompts
2. AI model inference with fallback
3. Post-processing and validation
4. Audit logging for all requests
"""
import hashlib
import logging
import time
from typing import Any
from uuid import uuid4

from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.core_models import Asset, GenerationLog, Scene
from ..schemas.generation import GenerationRequest, GenerationResponse
from ..services.context_builder import context_builder
from ..services.inference_client import inference_client
from ..services.postprocessor import postprocessor

logger = logging.getLogger(__name__)
router = APIRouter()


async def log_generation(
    db: Session,
    user_id: str,
    input_hash: str,
    prompt_hash: str,
    model_version: str,
    status: str,
    latency_ms: int,
    request_payload: dict[str, Any],
    response_payload: dict[str, Any] | None = None,
    error: str | None = None
) -> None:
    """
    Log generation request to database for audit and performance tracking

    Args:
        db: Database session
        user_id: User identifier
        input_hash: Hash of the complete input
        prompt_hash: Hash of the engineered prompt
        model_version: Model version used
        status: Status of the generation (success, fail_fallback, cached_fallback, error)
        latency_ms: Processing time in milliseconds
        request_payload: Original request data
        response_payload: Response data if successful
        error: Error message if failed
    """
    try:
        log_entry = GenerationLog(
            user_id=user_id,
            input_hash=input_hash,
            prompt_hash=prompt_hash,
            model_version=model_version,
            status=status,
            latency_ms=latency_ms,
            request_payload=request_payload,
            response_payload=response_payload,
            error=error
        )
        db.add(log_entry)
        db.commit()
        logger.info(f"Generation logged: {log_entry.id} - Status: {status}")
    except Exception as e:
        logger.error(f"Failed to log generation: {e}")
        db.rollback()


async def save_scene_to_db(
    db: Session,
    project_id: str,
    scene_data: dict[str, Any],
    generation_log_id: str | None = None
) -> None:
    """
    Save generated scene to database

    Args:
        db: Database session
        project_id: Project identifier
        scene_data: Complete scene data
        generation_log_id: Associated generation log ID
    """
    try:
        scene = Scene(
            project_id=project_id,
            name=scene_data.get("scene_name", "Untitled Scene"),
            style=scene_data.get("style", "platformer"),
            scene_data=scene_data,
            generation_log_id=generation_log_id
        )
        db.add(scene)
        db.commit()
        logger.info(f"Scene saved: {scene.id}")
    except Exception as e:
        logger.error(f"Failed to save scene: {e}")
        db.rollback()


@router.post("/", response_model=GenerationResponse)
async def generate_scene(
    request: GenerationRequest,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    """
    Generate a game scene from prompt with comprehensive logging

    This endpoint:
    1. Builds context from the user prompt and assets
    2. Calls the inference service (with automatic fallback)
    3. Post-processes the result
    4. Logs everything to the database
    5. Returns the generated scene
    """
    start_time = time.time()

    # Extract user ID (simplified for MVP - would come from auth in production)
    user_id = request.user_id or "anonymous"

    # Create input hash for deduplication
    input_data = f"{request.prompt}_{request.project_id}_{request.style or 'default'}"
    if request.assets:
        input_data += f"_{'_'.join(request.assets)}"
    input_hash = hashlib.sha256(input_data.encode()).hexdigest()[:16]

    try:
        # Step 1: Build context using ContextBuilder
        logger.info(f"Building context for project {request.project_id}")

        # Fetch assets from database if provided
        assets_data = []
        if request.assets:
            assets = db.query(Asset).filter(
                Asset.id.in_(request.assets),
                Asset.project_id == request.project_id
            ).all()
            assets_data = [asset.to_dict() for asset in assets]

        context = context_builder.build_generation_prompt(
            user_prompt=request.prompt,
            project_id=request.project_id,
            style=request.style,
            assets=assets_data,
            constraints=request.constraints
        )

        # Step 2: Call InferenceClient for generation
        logger.info(f"Generating scene with prompt hash: {context['prompt_hash']}")
        generation_result = await inference_client.generate_scene(
            context=context,
            model_version=request.model_version
        )

        # Step 3: Post-process the generated scene
        logger.info("Post-processing generated scene")
        processed_scene = postprocessor.process_scene(
            raw_scene=generation_result["scene"],
            project_id=request.project_id,
            assets=assets_data
        )

        # Validate the processed scene
        if not postprocessor.validate_scene(processed_scene):
            raise ValueError("Generated scene failed validation")

        # Enhance the scene with additional features
        enhanced_scene = postprocessor.enhance_scene(processed_scene)

        # Calculate total latency
        latency_ms = int((time.time() - start_time) * 1000)

        # Step 4: Log to database (in background)
        generation_log_id = str(uuid4())
        background_tasks.add_task(
            log_generation,
            db=db,
            user_id=user_id,
            input_hash=input_hash,
            prompt_hash=context["prompt_hash"],
            model_version=generation_result["metadata"]["model_version"],
            status=generation_result["metadata"]["status"],
            latency_ms=latency_ms,
            request_payload=request.dict(),
            response_payload=enhanced_scene
        )

        # Save scene to database (in background)
        background_tasks.add_task(
            save_scene_to_db,
            db=db,
            project_id=request.project_id,
            scene_data=enhanced_scene,
            generation_log_id=generation_log_id
        )

        # Step 5: Return response
        logger.info(f"Generation successful - Status: {generation_result['metadata']['status']}")
        return GenerationResponse(
            scene_id=enhanced_scene["id"],
            scene=enhanced_scene,
            generation_time=latency_ms / 1000.0,
            metadata={
                "status": generation_result["metadata"]["status"],
                "model_version": generation_result["metadata"]["model_version"],
                "use_local_model": generation_result["metadata"].get("use_local_model", False),
                "fallback_sample": generation_result["metadata"].get("fallback_sample"),
                "prompt_hash": context["prompt_hash"]
            }
        )

    except Exception as e:
        logger.error(f"Generation failed: {e}")
        latency_ms = int((time.time() - start_time) * 1000)

        # Log the error
        background_tasks.add_task(
            log_generation,
            db=db,
            user_id=user_id,
            input_hash=input_hash,
            prompt_hash=hashlib.sha256(request.prompt.encode()).hexdigest()[:16],
            model_version="error",
            status="error",
            latency_ms=latency_ms,
            request_payload=request.dict(),
            error=str(e)
        )

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}"
        ) from e


@router.get("/status")
async def get_generation_status():
    """
    Get the current status of the generation service

    Returns information about:
    - Model connectivity
    - Available golden samples
    - Service statistics
    """
    return inference_client.get_model_status()


@router.get("/samples")
async def list_golden_samples():
    """
    List all available golden samples

    Useful for testing and debugging
    """
    return {
        "samples": inference_client.list_golden_samples(),
        "total": len(inference_client.golden_samples)
    }


@router.get("/samples/{sample_name}")
async def get_golden_sample(sample_name: str):
    """
    Get a specific golden sample by name

    Args:
        sample_name: Name of the sample to retrieve
    """
    sample = inference_client.load_golden_sample(sample_name)
    if not sample:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Golden sample '{sample_name}' not found"
        )
    return sample
