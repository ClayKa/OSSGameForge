"""
Project schemas for OSSGameForge API
"""
from pydantic import BaseModel, Field
from typing import Optional

class ProjectBase(BaseModel):
    """Base project schema"""
    name: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)

class ProjectCreate(ProjectBase):
    """Schema for creating a project"""
    pass

class ProjectUpdate(ProjectBase):
    """Schema for updating a project"""
    name: Optional[str] = Field(None, min_length=1, max_length=100)

class ProjectResponse(ProjectBase):
    """Schema for project response"""
    id: str
    owner: str
    created_at: str
    updated_at: str
    assets_count: int = 0
    scenes_count: int = 0
    
    class Config:
        from_attributes = True

class Project(ProjectResponse):
    """Full project schema"""
    pass