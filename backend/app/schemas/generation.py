"""
Generation schemas for OSSGameForge API
"""

from enum import Enum
from typing import Any

from pydantic import BaseModel, Field


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

    gravity: bool | None = False
    collision: bool | None = True
    static: bool | None = False
    mass: float | None = 1.0


class Entity(BaseModel):
    """Game entity schema"""

    id: str
    type: EntityType
    name: str
    position: Position
    size: Size
    sprite: str | None = None
    color: str | None = None
    physics: Physics | None = None
    properties: dict[str, Any] | None = {}


class SceneMetadata(BaseModel):
    """Scene metadata"""

    width: int = 1920
    height: int = 1080
    background_color: str = "#87CEEB"
    theme: str | None = None
    used_assets: list[str] | None = []


class Scene(BaseModel):
    """Game scene schema"""

    id: str
    project_id: str
    name: str
    description: str
    version: str = "1.0.0"
    metadata: SceneMetadata
    entities: list[Entity]
    created_at: str


class GenerationRequest(BaseModel):
    """Request for scene generation"""

    prompt: str = Field(..., min_length=1, max_length=1000)
    project_id: str
    assets: list[str] | None = []
    style: GameStyle | None = None


class GenerationResponse(BaseModel):
    """Response for scene generation"""

    scene_id: str
    scene: Scene
    generation_time: float = Field(..., description="Generation time in seconds")
