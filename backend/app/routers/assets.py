"""
Assets router for OSSGameForge API
"""
import json
import logging
from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    BackgroundTasks,
    Depends,
    File,
    Form,
    HTTPException,
    UploadFile,
    status,
)
from sqlalchemy.orm import Session

from ..config import settings
from ..database import get_db
from ..schemas.asset import AssetResponse, AssetUploadResponse
from ..services import asset_service

router = APIRouter()
logger = logging.getLogger(__name__)

def load_mock_data():
    """Load mock data from JSON file"""
    mock_file = Path("/app/mocks/mock_data.json")
    if not mock_file.exists():
        # Fallback to devops/mocks directory
        mock_file = Path("/app/../devops/mocks/mock_data.json")

    if mock_file.exists():
        with open(mock_file) as f:
            return json.load(f)
    return {"projects": [], "assets": [], "scenes": []}

@router.post("/projects/{project_id}/assets", response_model=AssetUploadResponse, status_code=status.HTTP_202_ACCEPTED)
async def upload_asset(
    project_id: str,
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    user_consent: bool = Form(...),
    _tags: list[str] | None = Form(None),
    db: Session = Depends(get_db)
):
    """Upload a new asset with consent validation and EXIF stripping"""

    # Validate user consent - CRITICAL SECURITY CHECK
    if not user_consent:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User consent is mandatory and must be explicitly set to 'true'."
        )

    # Read file content
    file_content = await file.read()
    file_size = len(file_content)

    # Validate file size
    if file_size > settings.max_upload_size:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail=f"File size exceeds maximum allowed size of {settings.max_upload_size} bytes"
        )

    # Validate file type
    content_type = file.content_type or "application/octet-stream"
    if content_type.startswith("image/") and content_type not in settings.allowed_image_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Image type {content_type} is not supported"
        )
    elif content_type.startswith("audio/") and content_type not in settings.allowed_audio_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Audio type {content_type} is not supported"
        )
    elif content_type.startswith("video/") and content_type not in settings.allowed_video_types:
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail=f"Video type {content_type} is not supported"
        )

    if settings.mock_mode:
        # Create mock response
        asset_id = str(uuid4())
        logger.info(f"Mock mode: simulating asset upload for {file.filename}")
        return {
            "asset_id": asset_id,
            "status": "processing",
            "message": "Asset upload initiated (mock mode)"
        }

    try:
        # Create initial database record
        new_asset = asset_service.create_initial_asset_record(
            db=db,
            project_id=project_id,
            filename=file.filename,
            content_type=content_type,
            file_size=file_size
        )

        # Process and store the file (includes EXIF stripping for images)
        await asset_service.process_and_store_file(
            db=db,
            asset=new_asset,
            file_data=file_content,
            original_filename=file.filename
        )

        # Add background task for metadata extraction
        background_tasks.add_task(
            asset_service.extract_metadata_task,
            asset_id=str(new_asset.id)
        )

        logger.info(f"Asset {new_asset.id} uploaded successfully, processing in background")

        return {
            "asset_id": str(new_asset.id),
            "status": "processing",
            "message": "Asset upload initiated successfully"
        }

    except Exception as e:
        logger.error(f"Failed to upload asset: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process asset upload: {str(e)}"
        ) from e

@router.get("/projects/{project_id}/assets", response_model=list[AssetResponse])
async def list_project_assets(
    project_id: str,
    db: Session = Depends(get_db)
):
    """List all assets for a project"""
    if settings.mock_mode:
        data = load_mock_data()
        assets = data.get("assets", [])
        # Filter assets by project_id
        project_assets = [asset for asset in assets if asset.get("project_id") == project_id]
        return project_assets

    # Real implementation
    assets = asset_service.list_project_assets(db, project_id)
    return [
        {
            "id": str(asset.id),
            "project_id": asset.project_id,
            "type": asset.type,
            "status": asset.status,
            "path": asset.path,
            "metadata": asset.asset_metadata,
            "consent_hash": asset.consent_hash,
            "exif_stripped": asset.exif_stripped,
            "created_at": asset.created_at.isoformat() if asset.created_at else None,
            "updated_at": asset.updated_at.isoformat() if asset.updated_at else None
        }
        for asset in assets
    ]

@router.get("/assets/{asset_id}", response_model=AssetResponse)
async def get_asset(
    asset_id: str,
    db: Session = Depends(get_db)
):
    """Get asset details"""
    if settings.mock_mode:
        data = load_mock_data()
        assets = data.get("assets", [])
        for asset in assets:
            if asset["id"] == asset_id:
                return asset
        raise HTTPException(status_code=404, detail="Asset not found")

    # Real implementation
    asset = asset_service.get_asset_by_id(db, asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    return {
        "id": str(asset.id),
        "project_id": asset.project_id,
        "type": asset.type,
        "status": asset.status,
        "path": asset.path,
        "metadata": asset.metadata,
        "consent_hash": asset.consent_hash,
        "exif_stripped": asset.exif_stripped,
        "created_at": asset.created_at.isoformat() if asset.created_at else None,
        "updated_at": asset.updated_at.isoformat() if asset.updated_at else None
    }
