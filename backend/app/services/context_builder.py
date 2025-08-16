"""
Context Builder Service

This service is responsible for constructing prompts for AI generation.
It takes user input and project context to create optimized prompts
for the inference engine.
"""

import hashlib
import json
from typing import Any


class ContextBuilder:
    """Service for building generation contexts and prompts"""

    def __init__(self):
        self.max_context_length = 2048
        self.template_cache = {}

    def build_generation_prompt(
        self,
        user_prompt: str,
        project_id: str,
        assets: list[dict[str, Any]] | None = None,
        style: str | None = None,
        additional_context: dict[str, Any] | None = None,
        constraints: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        """
        Build a structured prompt for scene generation

        Args:
            user_prompt: The user's natural language prompt
            project_id: The project identifier
            assets: List of available assets with metadata
            style: The desired game style (platformer, rpg, etc.)
            additional_context: Any additional context parameters

        Returns:
            A structured prompt dictionary ready for inference
        """
        # Build base context
        context: dict[str, Any] = {
            "user_prompt": user_prompt,
            "project_id": project_id,
            "style": style or "platformer",
            "timestamp": self._get_timestamp(),
        }

        # Add asset context if provided
        if assets:
            context["assets"] = self._process_assets(assets)
            context["asset_count"] = len(assets)

        # Add constraints if provided
        if constraints:
            context["constraints"] = constraints

        # Add additional context
        if additional_context:
            context.update(additional_context)

        # Generate prompt hash for caching
        context["prompt_hash"] = self._generate_prompt_hash(context)

        # Apply prompt engineering techniques
        context["engineered_prompt"] = self._engineer_prompt(user_prompt, context)

        return context

    def build_editing_context(
        self, scene_id: str, modifications: dict[str, Any], current_scene: dict[str, Any]
    ) -> dict[str, Any]:
        """
        Build context for scene editing operations

        Args:
            scene_id: The scene identifier
            modifications: The requested modifications
            current_scene: The current scene state

        Returns:
            A structured context for scene editing
        """
        return {
            "scene_id": scene_id,
            "modifications": modifications,
            "current_state": current_scene,
            "operation": "edit",
            "timestamp": self._get_timestamp(),
        }

    def validate_context(self, context: dict[str, Any]) -> bool:
        """
        Validate that a context has all required fields

        Args:
            context: The context to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ["user_prompt", "project_id"]
        # Check not just presence but also non-None and non-empty values
        return all(
            field in context and context[field] is not None and context[field] != ""
            for field in required_fields
        )

    def _process_assets(self, assets: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Process and filter assets for context inclusion"""
        processed = []
        for asset in assets[:50]:  # Limit to prevent context overflow
            processed.append(
                {
                    "id": asset.get("id"),
                    "type": asset.get("type"),
                    "name": asset.get("name", ""),
                    "metadata": self._extract_relevant_metadata(asset.get("metadata", {})),
                }
            )
        return processed

    def _extract_relevant_metadata(self, metadata: dict[str, Any]) -> dict[str, Any]:
        """Extract only relevant metadata fields"""
        relevant_fields = ["width", "height", "duration", "format", "size"]
        return {k: v for k, v in metadata.items() if k in relevant_fields}

    def _engineer_prompt(self, user_prompt: str, context: dict[str, Any]) -> str:
        """Apply prompt engineering techniques"""
        style = context.get("style", "platformer")
        asset_count = context.get("asset_count", 0)

        engineered = (
            f"Create a {style} game scene based on the following description: {user_prompt}"
        )

        if asset_count > 0:
            engineered += f" The scene should incorporate {asset_count} available assets."

        engineered += " Generate a structured JSON scene with entities, positions, and properties."

        return engineered

    def _generate_prompt_hash(self, context: dict[str, Any]) -> str:
        """Generate a hash for prompt caching"""
        # Create a deterministic string representation
        hash_input = json.dumps(
            {
                "prompt": context.get("user_prompt", ""),
                "style": context.get("style", ""),
                "assets": len(context.get("assets", [])),
            },
            sort_keys=True,
        )

        return hashlib.sha256(hash_input.encode()).hexdigest()

    def _get_timestamp(self) -> str:
        """Get current timestamp"""
        from datetime import datetime, timezone

        return datetime.now(timezone.utc).isoformat()


# Module-level singleton instance
context_builder = ContextBuilder()
