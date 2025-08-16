"""
Postprocessor Service

This service processes AI output into valid scene JSON.
It handles validation, normalization, and enhancement of generated scenes.
"""
import uuid
from datetime import datetime, timezone
from typing import Any


class Postprocessor:
    """Service for processing and validating AI-generated scenes"""

    def __init__(self):
        self.validation_rules = self._initialize_validation_rules()
        self.default_properties = self._initialize_default_properties()

    def process_scene(
        self,
        raw_scene: dict[str, Any],
        project_id: str,
        assets: list[dict[str, Any]] | None = None
    ) -> dict[str, Any]:
        """
        Process raw AI output into a valid scene

        Args:
            raw_scene: The raw scene data from AI
            project_id: The project identifier
            assets: Available assets to incorporate

        Returns:
            A processed and validated scene
        """
        # Ensure scene has required fields
        processed_scene = self._ensure_required_fields(raw_scene, project_id)

        # Validate and normalize entities
        processed_scene["entities"] = self._process_entities(
            processed_scene.get("entities", [])
        )

        # Incorporate assets if provided
        if assets:
            processed_scene = self._incorporate_assets(processed_scene, assets)

        # Add metadata
        processed_scene["metadata"] = self._generate_metadata(processed_scene)

        # Validate final scene
        if not self.validate_scene(processed_scene):
            # If validation fails, return a minimal valid scene
            return self._create_minimal_scene(project_id)

        return processed_scene

    def validate_scene(self, scene: dict[str, Any]) -> bool:
        """
        Validate that a scene meets all requirements

        Args:
            scene: The scene to validate

        Returns:
            True if valid, False otherwise
        """
        # Check required fields
        required_fields = ["id", "name", "style", "entities"]
        if not all(field in scene for field in required_fields):
            return False

        # Validate entities
        if not isinstance(scene.get("entities"), list):
            return False

        return all(self._validate_entity(entity) for entity in scene["entities"])

    def enhance_scene(
        self,
        scene: dict[str, Any],
        enhancements: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        """
        Apply enhancements to an existing scene

        Args:
            scene: The scene to enhance
            enhancements: Optional enhancement parameters

        Returns:
            Enhanced scene
        """
        enhanced = scene.copy()

        # Apply default enhancements
        enhanced = self._add_physics_properties(enhanced)
        enhanced = self._add_collision_boundaries(enhanced)
        enhanced = self._optimize_entity_placement(enhanced)

        # Apply custom enhancements if provided
        if enhancements:
            if enhancements.get("add_lighting"):
                enhanced = self._add_lighting_system(enhanced)
            if enhancements.get("add_audio"):
                enhanced = self._add_audio_cues(enhanced)

        return enhanced

    def _ensure_required_fields(
        self,
        scene: dict[str, Any],
        project_id: str
    ) -> dict[str, Any]:
        """Ensure scene has all required fields"""
        if "id" not in scene:
            scene["id"] = f"scene_{uuid.uuid4().hex[:8]}"

        if "name" not in scene:
            scene["name"] = "Generated Scene"

        if "style" not in scene:
            scene["style"] = "platformer"

        if "entities" not in scene:
            scene["entities"] = []

        scene["project_id"] = project_id
        scene["created_at"] = datetime.now(timezone.utc).isoformat()

        return scene

    def _process_entities(self, entities: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process and validate entities"""
        processed = []

        for entity in entities:
            # Ensure entity has required fields
            if "id" not in entity:
                entity["id"] = f"entity_{uuid.uuid4().hex[:8]}"

            if "type" not in entity:
                entity["type"] = "object"

            # Ensure position
            if "position" not in entity:
                entity["position"] = {"x": 0, "y": 0}
            else:
                entity["position"] = self._normalize_position(entity["position"])

            # Ensure size
            if "size" not in entity:
                entity["size"] = self._get_default_size(entity["type"])
            else:
                entity["size"] = self._normalize_size(entity["size"])

            # Apply default properties based on type
            if "properties" not in entity:
                entity["properties"] = {}
            entity["properties"] = self._apply_default_properties(
                entity["type"],
                entity["properties"]
            )

            processed.append(entity)

        return processed

    def _validate_entity(self, entity: dict[str, Any]) -> bool:
        """Validate a single entity"""
        required = ["id", "type", "position", "size"]
        if not all(field in entity for field in required):
            return False

        # Validate position
        pos = entity.get("position", {})
        if not isinstance(pos, dict) or "x" not in pos or "y" not in pos:
            return False

        # Validate size
        size = entity.get("size", {})
        return not (not isinstance(size, dict) or "width" not in size or "height" not in size)

    def _normalize_position(self, position: Any) -> dict[str, float]:
        """Normalize position to standard format"""
        if isinstance(position, dict):
            try:
                x = position.get("x", 0)
                y = position.get("y", 0)
                # Handle None, empty string, or invalid values
                x = float(x) if x is not None and str(x).strip() else 0.0
                y = float(y) if y is not None and str(y).strip() else 0.0
                return {"x": x, "y": y}
            except (ValueError, TypeError):
                # If conversion fails, return default position
                return {"x": 0.0, "y": 0.0}
        return {"x": 0.0, "y": 0.0}

    def _normalize_size(self, size: Any) -> dict[str, float]:
        """Normalize size to standard format"""
        if isinstance(size, dict):
            return {
                "width": float(size.get("width", 32)),
                "height": float(size.get("height", 32))
            }
        return {"width": 32.0, "height": 32.0}

    def _get_default_size(self, entity_type: str) -> dict[str, float]:
        """Get default size for entity type"""
        defaults = {
            "player": {"width": 32, "height": 48},
            "enemy": {"width": 32, "height": 32},
            "platform": {"width": 100, "height": 20},
            "item": {"width": 16, "height": 16},
            "background": {"width": 800, "height": 600}
        }
        return defaults.get(entity_type, {"width": 32, "height": 32})

    def _apply_default_properties(
        self,
        entity_type: str,
        properties: dict[str, Any]
    ) -> dict[str, Any]:
        """Apply default properties based on entity type"""
        if entity_type not in self.default_properties:
            return properties

        defaults = self.default_properties[entity_type].copy()
        defaults.update(properties)
        return defaults

    def _incorporate_assets(
        self,
        scene: dict[str, Any],
        assets: list[dict[str, Any]]
    ) -> dict[str, Any]:
        """Incorporate available assets into the scene"""
        # Add asset references to scene
        scene["assets"] = []

        for asset in assets[:10]:  # Limit to prevent overload
            asset_ref = {
                "id": asset.get("id"),
                "type": asset.get("type"),
                "path": asset.get("path")
            }
            scene["assets"].append(asset_ref)

            # Try to assign assets to entities
            for entity in scene["entities"]:
                if entity["type"] == "player" and asset.get("type") == "image":
                    entity["properties"]["sprite"] = asset.get("path")
                    break

        return scene

    def _generate_metadata(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Generate scene metadata"""
        return {
            "entity_count": len(scene.get("entities", [])),
            "asset_count": len(scene.get("assets", [])),
            "style": scene.get("style", "unknown"),
            "version": "1.0.0",
            "processed_at": datetime.now(timezone.utc).isoformat()
        }

    def _create_minimal_scene(self, project_id: str) -> dict[str, Any]:
        """Create a minimal valid scene as fallback"""
        return {
            "id": f"scene_{uuid.uuid4().hex[:8]}",
            "name": "Minimal Scene",
            "project_id": project_id,
            "style": "platformer",
            "entities": [
                {
                    "id": "player_default",
                    "type": "player",
                    "position": {"x": 100, "y": 100},
                    "size": {"width": 32, "height": 48},
                    "properties": {"health": 100}
                }
            ],
            "metadata": {
                "entity_count": 1,
                "asset_count": 0,
                "style": "platformer",
                "version": "1.0.0"
            }
        }

    def _add_physics_properties(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Add physics properties to entities"""
        for entity in scene.get("entities", []):
            # Ensure properties field exists
            if "properties" not in entity:
                entity["properties"] = {}

            if "physics" not in entity["properties"]:
                # Add comprehensive physics properties
                entity["properties"]["physics"] = {
                    "gravity": entity["type"] != "platform",
                    "collision": True,
                    "mass": 1.0 if entity["type"] == "player" else 0.0 if entity["type"] == "platform" else 0.5,
                    "friction": 0.8,
                    "restitution": 0.2
                }
        return scene

    def _add_collision_boundaries(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Add collision boundaries to entities"""
        for entity in scene.get("entities", []):
            if "collision_box" not in entity:
                entity["collision_box"] = {
                    "offset": {"x": 0, "y": 0},
                    "size": entity["size"].copy()
                }
        return scene

    def _optimize_entity_placement(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Optimize entity placement to prevent overlaps"""
        # Simple optimization - ensure minimum spacing
        entities = scene.get("entities", [])
        for i, entity in enumerate(entities):
            for _j, other in enumerate(entities[i+1:], i+1):
                if self._entities_overlap(entity, other):
                    # Move the second entity
                    other["position"]["x"] += entity["size"]["width"] + 10
        return scene

    def _entities_overlap(self, e1: dict[str, Any], e2: dict[str, Any]) -> bool:
        """Check if two entities overlap"""
        # Simple AABB collision check
        return (
            e1["position"]["x"] < e2["position"]["x"] + e2["size"]["width"] and
            e1["position"]["x"] + e1["size"]["width"] > e2["position"]["x"] and
            e1["position"]["y"] < e2["position"]["y"] + e2["size"]["height"] and
            e1["position"]["y"] + e1["size"]["height"] > e2["position"]["y"]
        )

    def _add_lighting_system(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Add lighting system to scene"""
        scene["lighting"] = {
            "ambient": {"color": "#ffffff", "intensity": 0.5},
            "directional": {"color": "#ffff00", "intensity": 0.8, "angle": 45}
        }
        return scene

    def _add_audio_cues(self, scene: dict[str, Any]) -> dict[str, Any]:
        """Add audio cues to scene"""
        scene["audio"] = {
            "background_music": "assets/audio/theme.mp3",
            "ambient_sounds": ["assets/audio/wind.mp3"]
        }
        return scene

    def _initialize_validation_rules(self) -> dict[str, Any]:
        """Initialize validation rules"""
        return {
            "max_entities": 100,
            "max_scene_size": {"width": 10000, "height": 10000},
            "valid_entity_types": ["player", "enemy", "platform", "item", "background", "object"],
            "valid_styles": ["platformer", "rpg", "puzzle", "adventure"]
        }

    def _initialize_default_properties(self) -> dict[str, dict[str, Any]]:
        """Initialize default properties for entity types"""
        return {
            "player": {"health": 100, "speed": 5, "jump_power": 10},
            "enemy": {"health": 50, "damage": 10, "speed": 3},
            "platform": {"solid": True, "friction": 0.8},
            "item": {"collectable": True, "value": 1},
            "background": {"parallax": False, "depth": 0}
        }


# Module-level singleton instance
postprocessor = Postprocessor()
