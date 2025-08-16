"""
Projects router for OSSGameForge API
"""
from fastapi import APIRouter, HTTPException, status
from typing import List
import json
from pathlib import Path
from uuid import uuid4
from datetime import datetime

from ..config import settings
from ..schemas.project import ProjectCreate, ProjectResponse

router = APIRouter()

def load_mock_data():
    """Load mock data from JSON file"""
    mock_file = Path("/app/mocks/mock_data.json")
    if not mock_file.exists():
        # Fallback to devops/mocks directory
        mock_file = Path("/app/../devops/mocks/mock_data.json")
    
    if mock_file.exists():
        with open(mock_file, 'r') as f:
            return json.load(f)
    return {"projects": [], "assets": [], "scenes": []}

@router.get("/", response_model=List[ProjectResponse])
async def list_projects():
    """List all projects"""
    if settings.mock_mode:
        data = load_mock_data()
        return data.get("projects", [])
    
    # TODO: Implement real database query
    return []

@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
async def create_project(project: ProjectCreate):
    """Create a new project"""
    if settings.mock_mode:
        # Create mock response
        new_project = {
            "id": f"proj_{uuid4().hex[:8]}",
            "name": project.name,
            "description": project.description or "",
            "owner": "demo_user",
            "created_at": datetime.utcnow().isoformat() + "Z",
            "updated_at": datetime.utcnow().isoformat() + "Z",
            "assets_count": 0,
            "scenes_count": 0
        }
        return new_project
    
    # TODO: Implement real project creation
    raise HTTPException(status_code=501, detail="Real mode not implemented yet")

@router.get("/{project_id}", response_model=ProjectResponse)
async def get_project(project_id: str):
    """Get project details"""
    if settings.mock_mode:
        data = load_mock_data()
        projects = data.get("projects", [])
        for project in projects:
            if project["id"] == project_id:
                return project
        raise HTTPException(status_code=404, detail="Project not found")
    
    # TODO: Implement real database query
    raise HTTPException(status_code=501, detail="Real mode not implemented yet")