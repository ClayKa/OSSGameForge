"""
Inference Client Service

This service handles model inference with fallback mechanisms.
It can use either a local model or fallback to predefined samples
based on the USE_LOCAL_MODEL environment variable.

Key Features:
- Automatic fallback to golden samples when model is unavailable
- Intelligent sample selection based on prompt keywords
- Comprehensive error handling and status tracking
- Performance monitoring with latency tracking
"""
import os
import json
import time
import random
import hashlib
import logging
import asyncio
from typing import Dict, Any, Optional, List, Tuple
from pathlib import Path
from datetime import datetime, timezone

logger = logging.getLogger(__name__)


class InferenceClient:
    """Service for handling AI model inference with fallback mechanism"""
    
    def __init__(self):
        self.use_local_model = os.getenv("USE_LOCAL_MODEL", "false").lower() == "true"
        self.model_endpoint = os.getenv("MODEL_ENDPOINT", "http://localhost:11434")
        self.model_timeout = int(os.getenv("MODEL_TIMEOUT", "45"))
        self.model_name = os.getenv("MODEL_NAME", "gpt-oss-20b")
        
        # Fix path for golden samples
        self.golden_samples_path = Path(__file__).parent.parent / "golden_samples"
        self.golden_samples = []
        self._load_golden_samples()
        
        # Track statistics
        self.stats = {
            "total_requests": 0,
            "model_successes": 0,
            "model_failures": 0,
            "fallback_uses": 0,
            "last_request_time": None
        }
    
    def _load_golden_samples(self):
        """Load golden samples for fallback mode"""
        self.golden_samples = []
        
        # Define keywords for intelligent sample selection
        sample_metadata = {
            "sample_simple_geometry.json": {
                "keywords": ["simple", "basic", "geometry", "platform", "block", "minimal", "test"],
                "complexity": 1,
                "description": "Basic geometric shapes and simple platformer elements"
            },
            "sample_asset_intensive.json": {
                "keywords": ["asset", "texture", "sprite", "image", "audio", "resource", "forest", "animated", "detailed"],
                "complexity": 2,
                "description": "Asset-heavy scene with textures, sprites, and audio resources"
            },
            "sample_complex_structure.json": {
                "keywords": ["complex", "advanced", "layer", "nested", "puzzle", "mechanism", "trigger", "event", "script"],
                "complexity": 3,
                "description": "Complex nested structures with layers, events, and scripts"
            },
            "sample_minimal_empty.json": {
                "keywords": ["empty", "blank", "none", "minimal", "sandbox", "clean", "start"],
                "complexity": 0,
                "description": "Empty scene for testing edge cases and sandbox initialization"
            },
            "sample_single_entity.json": {
                "keywords": ["single", "one", "solo", "minimal", "basic", "simple"],
                "complexity": 0.5,
                "description": "Minimal viable scene with a single entity"
            }
        }
        
        # Try to load from files
        if self.golden_samples_path.exists():
            logger.info(f"Loading golden samples from {self.golden_samples_path}")
            
            for sample_file in self.golden_samples_path.glob("sample_*.json"):
                try:
                    with open(sample_file, 'r') as f:
                        sample_data = json.load(f)
                        
                        # Add metadata for intelligent selection
                        file_name = sample_file.name
                        if file_name in sample_metadata:
                            meta = sample_metadata[file_name]
                            sample_entry = {
                                "name": file_name.replace(".json", ""),
                                "keywords": meta["keywords"],
                                "complexity": meta["complexity"],
                                "description": meta["description"],
                                "data": sample_data
                            }
                        else:
                            # Fallback for unknown samples
                            sample_entry = {
                                "name": file_name.replace(".json", ""),
                                "keywords": [],
                                "complexity": 1,
                                "description": "Custom golden sample",
                                "data": sample_data
                            }
                        
                        self.golden_samples.append(sample_entry)
                        logger.info(f"Loaded golden sample: {file_name}")
                        
                except Exception as e:
                    logger.error(f"Failed to load golden sample {sample_file}: {e}")
        else:
            logger.warning(f"Golden samples directory not found: {self.golden_samples_path}")
        
        # Log summary
        if self.golden_samples:
            logger.info(f"Successfully loaded {len(self.golden_samples)} golden samples")
        else:
            logger.error("No golden samples loaded - using minimal fallback")
    
    async def generate_scene(
        self,
        context: Dict[str, Any],
        model_version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Generate a scene based on the provided context
        
        Args:
            context: The generation context from ContextBuilder
            model_version: Optional specific model version to use
            
        Returns:
            Generated scene data with metadata including status tracking
        """
        start_time = time.time()
        self.stats["total_requests"] += 1
        self.stats["last_request_time"] = datetime.now(timezone.utc).isoformat()
        
        status = "success"
        fallback_reason = None
        selected_sample = None
        
        try:
            if self.use_local_model:
                logger.info(f"Attempting local model generation with {self.model_name}")
                try:
                    result = await self._call_local_model(context, model_version)
                    self.stats["model_successes"] += 1
                    status = "success"
                except Exception as model_error:
                    logger.warning(f"Local model failed, using fallback: {model_error}")
                    result, selected_sample = self._use_fallback_sample(context)
                    self.stats["model_failures"] += 1
                    self.stats["fallback_uses"] += 1
                    status = "fail_fallback"
                    fallback_reason = str(model_error)
            else:
                logger.info("Using fallback mode (USE_LOCAL_MODEL=false)")
                result, selected_sample = self._use_fallback_sample(context)
                self.stats["fallback_uses"] += 1
                status = "cached_fallback"
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            metadata = {
                "model_version": model_version or self.model_name if self.use_local_model else "fallback",
                "latency_ms": latency_ms,
                "use_local_model": self.use_local_model,
                "prompt_hash": context.get("prompt_hash"),
                "status": status,
                "timestamp": datetime.now(timezone.utc).isoformat()
            }
            
            if selected_sample:
                metadata["fallback_sample"] = selected_sample
                
            if fallback_reason:
                metadata["fallback_reason"] = fallback_reason
            
            return {
                "scene": result,
                "metadata": metadata
            }
            
        except Exception as e:
            logger.error(f"Critical error in scene generation: {e}")
            latency_ms = int((time.time() - start_time) * 1000)
            self.stats["model_failures"] += 1
            
            # On error, return a minimal valid scene
            return {
                "scene": self._get_error_fallback_scene(),
                "metadata": {
                    "model_version": "error_fallback",
                    "latency_ms": latency_ms,
                    "use_local_model": self.use_local_model,
                    "status": "error",
                    "error": str(e),
                    "timestamp": datetime.now(timezone.utc).isoformat()
                }
            }
    
    async def _call_local_model(
        self,
        context: Dict[str, Any],
        model_version: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Call the local model endpoint (Ollama or similar)
        
        This attempts to connect to a local model server.
        In production, this would make an HTTP request to the model server.
        For now, it simulates the connection attempt and falls back gracefully.
        """
        import httpx
        
        # Prepare the prompt for the model
        prompt = context.get("engineered_prompt", context.get("user_prompt", ""))
        
        # Construct the request payload
        payload = {
            "model": model_version or self.model_name,
            "prompt": f"""Generate a game scene JSON for the following request:
{prompt}

The scene should include entities, positions, sizes, and properties.
Return only valid JSON without any explanation.""",
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "max_tokens": 2048
            }
        }
        
        try:
            # Attempt to call the local model
            async with httpx.AsyncClient(timeout=self.model_timeout) as client:
                response = await client.post(
                    f"{self.model_endpoint}/api/generate",
                    json=payload
                )
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                scene_json = json.loads(result.get("response", "{}"))
                
                logger.info("Successfully generated scene from local model")
                return scene_json
                
        except httpx.ConnectError:
            raise ConnectionError(f"Cannot connect to model at {self.model_endpoint}")
        except httpx.TimeoutException:
            raise TimeoutError(f"Model request timed out after {self.model_timeout}s")
        except Exception as e:
            raise RuntimeError(f"Model inference failed: {e}")
    
    def _use_fallback_sample(self, context: Dict[str, Any]) -> Tuple[Dict[str, Any], str]:
        """
        Select and return an appropriate golden sample based on context
        
        Returns:
            Tuple of (scene_data, sample_name)
        """
        if not self.golden_samples:
            logger.warning("No golden samples available, using error fallback")
            return self._get_error_fallback_scene(), "error_fallback"
        
        user_prompt = context.get("engineered_prompt", context.get("user_prompt", "")).lower()
        
        # Score each sample based on keyword matching
        scores = []
        for sample in self.golden_samples:
            score = 0
            for keyword in sample["keywords"]:
                if keyword in user_prompt:
                    score += 2  # Exact keyword match
                elif any(word in user_prompt for word in keyword.split()):
                    score += 1  # Partial match
            
            # Add complexity preference based on prompt
            if "simple" in user_prompt or "basic" in user_prompt:
                score += (4 - sample["complexity"])  # Prefer simpler samples
            elif "complex" in user_prompt or "advanced" in user_prompt:
                score += sample["complexity"]  # Prefer complex samples
            
            scores.append((score, sample))
        
        # Sort by score and get the best match
        scores.sort(key=lambda x: x[0], reverse=True)
        
        if scores[0][0] > 0:
            # We have a match based on keywords
            selected = scores[0][1]
            logger.info(f"Selected golden sample '{selected['name']}' with score {scores[0][0]}")
        else:
            # No keyword match, select based on complexity or random
            if "complex" in user_prompt:
                selected = max(self.golden_samples, key=lambda x: x["complexity"])
            elif "simple" in user_prompt:
                selected = min(self.golden_samples, key=lambda x: x["complexity"])
            else:
                selected = random.choice(self.golden_samples)
            logger.info(f"Selected golden sample '{selected['name']}' (no keyword match)")
        
        return selected["data"], selected["name"]
    
    def _get_error_fallback_scene(self) -> Dict[str, Any]:
        """Return a minimal valid scene for error cases"""
        return {
            "id": f"scene_error_{int(time.time())}",
            "scene_name": "Error Fallback Scene",
            "description": "Minimal scene generated due to processing error",
            "style": "platformer",
            "metadata": {
                "width": 800,
                "height": 600,
                "background_color": "#333333",
                "error_fallback": True
            },
            "entities": [
                {
                    "id": "player_default",
                    "type": "player",
                    "name": "Default Player",
                    "position": {"x": 100, "y": 300},
                    "size": {"width": 32, "height": 48},
                    "properties": {
                        "health": 100,
                        "color": "#FF0000"
                    }
                },
                {
                    "id": "platform_default",
                    "type": "platform",
                    "name": "Default Ground",
                    "position": {"x": 0, "y": 400},
                    "size": {"width": 800, "height": 200},
                    "properties": {
                        "color": "#654321",
                        "collision": True
                    }
                }
            ]
        }
    
    def get_model_status(self) -> Dict[str, Any]:
        """Get current model status and configuration"""
        status = {
            "use_local_model": self.use_local_model,
            "model_endpoint": self.model_endpoint if self.use_local_model else None,
            "model_name": self.model_name if self.use_local_model else None,
            "model_timeout": self.model_timeout,
            "fallback_samples_loaded": len(self.golden_samples),
            "golden_samples": [
                {
                    "name": sample["name"],
                    "complexity": sample["complexity"],
                    "description": sample["description"]
                }
                for sample in self.golden_samples
            ],
            "status": "ready" if self.golden_samples else "degraded",
            "statistics": self.stats
        }
        
        # Check model connectivity if local model is enabled
        if self.use_local_model:
            try:
                import httpx
                # Quick connectivity check (synchronous for status endpoint)
                with httpx.Client(timeout=2.0) as client:
                    response = client.get(f"{self.model_endpoint}/api/tags")
                    if response.status_code == 200:
                        status["model_connectivity"] = "connected"
                    else:
                        status["model_connectivity"] = "unreachable"
            except:
                status["model_connectivity"] = "disconnected"
        
        return status
    
    def load_golden_sample(self, sample_name: str) -> Optional[Dict[str, Any]]:
        """
        Load a specific golden sample by name
        
        Args:
            sample_name: Name of the sample to load
            
        Returns:
            The sample data or None if not found
        """
        for sample in self.golden_samples:
            if sample["name"] == sample_name:
                return sample["data"]
        return None
    
    def list_golden_samples(self) -> List[Dict[str, Any]]:
        """
        List all available golden samples
        
        Returns:
            List of sample metadata
        """
        return [
            {
                "name": sample["name"],
                "complexity": sample["complexity"],
                "description": sample["description"],
                "keywords": sample["keywords"]
            }
            for sample in self.golden_samples
        ]


# Module-level singleton instance
inference_client = InferenceClient()