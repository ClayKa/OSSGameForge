"""
Generation schemas for OSSGameForge API
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from enum import Enum

class GameStyle(str, Enum):
    """Game style enumeration"""
    PLATFORMER = "platformer"
    SHOOTER = "shooter"
    PUZZLE = "puzzle"
    RPG = "rpg"

class EntityType(str, Enum):
    """Entity type enumeration"""
    PLAYER = "player"
    PLATFORM = "platform"
    ENEMY = "enemy"
    COLLECTIBLE = "collectible"
    GOAL = "goal"
    OBSTACLE = "obstacle"

class Position(BaseModel):
    """Position in 2D space"""
    x: float
    y: float

class Size(BaseModel):
    """Size in 2D space"""
    width: float
    height: float

class Physics(BaseModel):
    """Physics properties"""
    gravity: Optional[bool] = False
    collision: Optional[bool] = True
    static: Optional[bool] = False
    mass: Optional[float] = 1.0

class Entity(BaseModel):
    """Game entity schema"""
    id: str
    type: EntityType
    name: str
    position: Position
    size: Size
    sprite: Optional[str] = None
    color: Optional[str] = None
    physics: Optional[Physics] = None
    properties: Optional[Dict[str, Any]] = {}

class SceneMetadata(BaseModel):
    """Scene metadata"""
    width: int = 1920
    height: int = 1080
    background_color: str = "#87CEEB"
    theme: Optional[str] = None
    used_assets: Optional[List[str]] = []

class Scene(BaseModel):
    """Game scene schema"""
    id: str
    project_id: str
    name: str
    description: str
    version: str = "1.0.0"
    metadata: SceneMetadata
    entities: List[Entity]
    created_at: str

class GenerationRequest(BaseModel):
    """Request for scene generation"""
    prompt: str = Field(..., min_length=1, max_length=1000)
    project_id: str
    assets: Optional[List[str]] = []
    style: Optional[GameStyle] = None

class GenerationResponse(BaseModel):
    """Response for scene generation"""
    scene_id: str
    scene: Scene
    generation_time: float = Field(..., description="Generation time in seconds")