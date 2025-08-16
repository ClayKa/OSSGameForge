"""
Asset schemas for OSSGameForge API
"""
from enum import Enum
from typing import Any

from pydantic import BaseModel


class AssetType(str, Enum):
    """Asset type enumeration"""
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    MODEL = "model"

class AssetStatus(str, Enum):
    """Asset processing status"""
    PROCESSING = "processing"
    PROCESSED = "processed"
    FAILED = "failed"

class AssetBase(BaseModel):
    """Base asset schema"""
    filename: str
    type: AssetType

class AssetUploadResponse(BaseModel):
    """Response for asset upload"""
    asset_id: str
    status: AssetStatus
    message: str = "Asset upload initiated"

class AssetResponse(BaseModel):
    """Schema for asset response"""
    id: str
    project_id: str
    filename: str
    path: str
    type: AssetType
    status: AssetStatus
    metadata: dict[str, Any] | None = {}
    consent_hash: str
    exif_stripped: bool
    created_at: str

    class Config:
        from_attributes = True

class Asset(AssetResponse):
    """Full asset schema"""
    pass
