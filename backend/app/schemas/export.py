"""
Export schemas for OSSGameForge API
"""
from enum import Enum

from pydantic import BaseModel, Field


class ExportEngine(str, Enum):
    """Export engine enumeration"""
    HTML5 = "html5"
    GODOT = "godot"
    UNITY = "unity"

class ExportRequest(BaseModel):
    """Request for scene export"""
    scene_id: str = Field(..., description="The scene ID to export")
    include_assets: bool = Field(default=True, description="Include assets in export")
