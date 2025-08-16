"""
Asset Service for OSSGameForge

Handles asset processing including:
- File storage to MinIO
- EXIF stripping for privacy protection
- Metadata extraction from various file types
- Async processing with database management
"""

import hashlib
import io
import logging
import tempfile
import time
from pathlib import Path

import tinytag
from PIL import Image
from sqlalchemy.orm import Session

from ..database import SessionLocal
from ..models import Asset
from ..storage import download_file_from_storage, minio_client, upload_file_to_storage

logger = logging.getLogger(__name__)


def create_initial_asset_record(
    db: Session, project_id: str, filename: str, content_type: str, file_size: int = 0
) -> Asset:
    """
    Create initial asset record in database

    Args:
        db: Database session
        project_id: Project identifier
        filename: Original filename
        content_type: MIME type of the file
        file_size: Size of the file in bytes

    Returns:
        Created Asset model instance
    """
    # Create consent hash for tracking
    user_id = "user_placeholder_123"  # TODO: Get from auth context
    consent_hash = hashlib.sha256(f"{user_id}{filename}{time.time()}".encode()).hexdigest()

    # Determine asset type from content type
    asset_type = _determine_asset_type(content_type)

    # Create new asset record
    new_asset = Asset(
        project_id=project_id,
        path="pending",  # Will be updated after storage
        type=asset_type,
        status="uploading",
        consent_hash=consent_hash,
        exif_stripped=False,
        asset_metadata={
            "original_filename": filename,
            "content_type": content_type,
            "file_size": file_size,
        },
    )

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    logger.info(f"Created asset record: {new_asset.id}")
    return new_asset


def _determine_asset_type(content_type: str) -> str:
    """Determine asset type from MIME type"""
    if content_type.startswith("image/"):
        return "image"
    elif content_type.startswith("audio/"):
        return "audio"
    elif content_type.startswith("video/"):
        return "video"
    elif content_type.startswith("model/") or content_type.endswith("gltf"):
        return "model"
    else:
        return "other"


async def process_and_store_file(
    db: Session, asset: Asset, file_data: bytes, original_filename: str
) -> str:
    """
    Process and store uploaded file

    Args:
        db: Database session
        asset: Asset model instance
        file_data: Raw file data
        original_filename: Original filename

    Returns:
        Storage path in MinIO
    """
    # Generate storage path
    file_extension = Path(original_filename).suffix
    storage_path = f"projects/{asset.project_id}/assets/{asset.id}{file_extension}"

    try:
        # Process based on file type
        if asset.type == "image":
            processed_data = await _process_image(file_data, asset)
            asset.exif_stripped = True
        else:
            processed_data = file_data

        # Upload to MinIO
        bucket_name = "ossgameforge-assets"
        _ensure_bucket_exists(bucket_name)

        upload_file_to_storage(
            bucket_name=bucket_name,
            object_name=storage_path,
            data=io.BytesIO(processed_data),
            length=len(processed_data),
            content_type=asset.asset_metadata.get("content_type", "application/octet-stream"),
        )

        # Update asset record
        asset.path = storage_path
        asset.status = "uploaded"
        db.commit()

        logger.info(f"Stored asset {asset.id} at {storage_path}")
        return storage_path

    except Exception as e:
        logger.error(f"Failed to process and store asset {asset.id}: {e}")
        asset.status = "error"
        asset.asset_metadata["error"] = str(e)
        db.commit()
        raise


async def _process_image(file_data: bytes, asset: Asset) -> bytes:
    """
    Process image file to strip EXIF data

    Args:
        file_data: Raw image data
        asset: Asset model instance

    Returns:
        Processed image data without EXIF
    """
    try:
        # Open image from bytes
        image = Image.open(io.BytesIO(file_data))

        # Store basic metadata before stripping
        asset.asset_metadata.update(
            {
                "width": image.width,
                "height": image.height,
                "format": image.format,
                "mode": image.mode,
            }
        )

        # Strip EXIF data by creating new image
        # This removes all metadata including EXIF, IPTC, and XMP
        if image.mode in ("RGBA", "LA", "P"):
            # Handle images with transparency
            clean_image = Image.new(image.mode, image.size)
            clean_image.putdata(list(image.getdata()))
        else:
            # Convert to RGB for consistent processing
            if image.mode != "RGB":
                image = image.convert("RGB")
            clean_image = Image.new("RGB", image.size)
            clean_image.putdata(list(image.getdata()))

        # Save to bytes
        output = io.BytesIO()
        save_format = asset.asset_metadata.get("format", "JPEG")
        if save_format == "JPEG":
            clean_image.save(output, format=save_format, quality=95, optimize=True)
        else:
            clean_image.save(output, format=save_format)

        return output.getvalue()

    except Exception as e:
        logger.error(f"Failed to process image: {e}")
        raise


def _ensure_bucket_exists(bucket_name: str):
    """Ensure MinIO bucket exists, create if not"""
    try:
        if not minio_client.bucket_exists(bucket_name):
            minio_client.make_bucket(bucket_name)
            logger.info(f"Created bucket: {bucket_name}")
    except Exception as e:
        logger.warning(f"Could not ensure bucket exists: {e}")


def extract_metadata_task(asset_id: str):
    """
    Background task to extract metadata from asset

    Args:
        asset_id: UUID of the asset to process
    """
    # Create new database session for background task
    db = SessionLocal()
    try:
        # Fetch asset record
        asset = db.query(Asset).filter(Asset.id == asset_id).first()
        if not asset:
            logger.error(f"Asset {asset_id} not found")
            return

        # Skip if already processed or errored
        if asset.status in ["processed", "error"]:
            return

        logger.info(f"Extracting metadata for asset {asset_id}")

        # Download file from storage for processing
        bucket_name = "ossgameforge-assets"

        with tempfile.NamedTemporaryFile(delete=True) as temp_file:
            try:
                # Download to temp file
                file_data = download_file_from_storage(
                    bucket_name=bucket_name, object_name=asset.path
                )
                temp_file.write(file_data)
                temp_file.flush()

                # Extract metadata based on type
                if asset.type == "audio":
                    _extract_audio_metadata(asset, temp_file.name, db)
                elif asset.type == "video":
                    _extract_video_metadata(asset, temp_file.name, db)
                elif asset.type == "image":
                    # Image metadata already extracted during upload
                    pass

                # Update status
                if asset.status != "error":
                    asset.status = "processed"
                    db.commit()
                    logger.info(f"Successfully processed asset {asset_id}")

            except Exception as e:
                logger.error(f"Failed to extract metadata for asset {asset_id}: {e}")
                asset.status = "error"
                asset.asset_metadata["error"] = str(e)
                db.commit()

    finally:
        db.close()


def _extract_audio_metadata(asset: Asset, file_path: str, db: Session):
    """Extract metadata from audio file"""
    try:
        tag = tinytag.TinyTag.get(file_path)

        # Extract essential metadata
        metadata = {
            "duration_seconds": tag.duration,
            "bitrate": tag.bitrate,
            "samplerate": tag.samplerate,
            "channels": tag.channels,
        }

        # Add optional metadata if available
        if tag.artist:
            metadata["artist"] = tag.artist
        if tag.title:
            metadata["title"] = tag.title
        if tag.album:
            metadata["album"] = tag.album

        # Update asset metadata
        asset.asset_metadata.update(metadata)
        db.commit()

        logger.info(f"Extracted audio metadata for asset {asset.id}")

    except Exception as e:
        logger.error(f"Failed to extract audio metadata: {e}")
        raise


def _extract_video_metadata(asset: Asset, file_path: str, db: Session):
    """Extract metadata from video file"""
    try:
        # For MVP, we'll use tinytag for basic video metadata
        # In production, you might want to use ffprobe or similar
        tag = tinytag.TinyTag.get(file_path)

        metadata = {
            "duration_seconds": tag.duration,
            "bitrate": tag.bitrate,
        }

        # Update asset metadata
        asset.asset_metadata.update(metadata)
        db.commit()

        logger.info(f"Extracted video metadata for asset {asset.id}")

    except Exception as e:
        logger.error(f"Failed to extract video metadata: {e}")
        raise


def get_asset_by_id(db: Session, asset_id: str) -> Asset | None:
    """
    Retrieve asset by ID

    Args:
        db: Database session
        asset_id: Asset UUID

    Returns:
        Asset instance or None
    """
    return db.query(Asset).filter(Asset.id == asset_id).first()


def list_project_assets(db: Session, project_id: str) -> list:
    """
    List all assets for a project

    Args:
        db: Database session
        project_id: Project identifier

    Returns:
        List of assets
    """
    return db.query(Asset).filter(Asset.project_id == project_id).all()


def update_asset_status(db: Session, asset_id: str, status: str, metadata: dict | None = None):
    """
    Update asset status and optionally metadata

    Args:
        db: Database session
        asset_id: Asset UUID
        status: New status
        metadata: Optional metadata to merge
    """
    asset = get_asset_by_id(db, asset_id)
    if asset:
        asset.status = status
        if metadata:
            asset.asset_metadata.update(metadata)
        db.commit()
        logger.info(f"Updated asset {asset_id} status to {status}")
