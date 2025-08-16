"""
Export router for OSSGameForge API
"""
import io
import json
import zipfile
from datetime import datetime
from pathlib import Path

from fastapi import APIRouter, HTTPException, Query, status
from fastapi.responses import StreamingResponse

from ..config import settings
from ..schemas.export import ExportEngine, ExportRequest

router = APIRouter()

def load_mock_data():
    """Load mock data from JSON file"""
    mock_file = Path("/app/mocks/mock_data.json")
    if not mock_file.exists():
        # Fallback to devops/mocks directory
        mock_file = Path("/app/../devops/mocks/mock_data.json")

    if mock_file.exists():
        with open(mock_file) as f:
            return json.load(f)
    return {"projects": [], "assets": [], "scenes": []}

def create_html5_export(scene_data: dict) -> bytes:
    """Create a simple HTML5 export package"""

    # Create HTML5 runner template
    html_content = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>OSSGameForge - {title}</title>
    <style>
        body {{
            margin: 0;
            padding: 0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #222;
            font-family: Arial, sans-serif;
        }}
        #gameCanvas {{
            border: 2px solid #444;
            background: {bg_color};
        }}
        .info {{
            position: absolute;
            top: 10px;
            left: 10px;
            color: white;
            font-size: 14px;
        }}
    </style>
</head>
<body>
    <div class="info">
        <h3>{title}</h3>
        <p>{description}</p>
        <p>Use arrow keys to move (mock export)</p>
    </div>
    <canvas id="gameCanvas" width="{width}" height="{height}"></canvas>
    <script>
        const sceneData = {scene_json};
        const canvas = document.getElementById('gameCanvas');
        const ctx = canvas.getContext('2d');

        // Simple render function
        function render() {{
            ctx.clearRect(0, 0, canvas.width, canvas.height);

            // Render entities
            if (sceneData.entities) {{
                sceneData.entities.forEach(entity => {{
                    if (entity.color) {{
                        ctx.fillStyle = entity.color;
                        ctx.fillRect(
                            entity.position.x,
                            entity.position.y,
                            entity.size.width,
                            entity.size.height
                        );
                    }}

                    // Draw entity name
                    ctx.fillStyle = 'white';
                    ctx.font = '12px Arial';
                    ctx.fillText(
                        entity.name || entity.type,
                        entity.position.x,
                        entity.position.y - 5
                    );
                }});
            }}
        }}

        // Initial render
        render();

        // Simple game loop
        function gameLoop() {{
            render();
            requestAnimationFrame(gameLoop);
        }}

        gameLoop();
    </script>
</body>
</html>""".format(
        title=scene_data.get("name", "Untitled Game"),
        description=scene_data.get("description", ""),
        width=scene_data.get("metadata", {}).get("width", 1920),
        height=scene_data.get("metadata", {}).get("height", 1080),
        bg_color=scene_data.get("metadata", {}).get("background_color", "#87CEEB"),
        scene_json=json.dumps(scene_data)
    )

    # Create a zip file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add HTML file
        zip_file.writestr("index.html", html_content)

        # Add scene data as separate JSON
        zip_file.writestr("scene.json", json.dumps(scene_data, indent=2))

        # Add a simple README
        readme_content = f"""# {scene_data.get("name", "OSSGameForge Game")}

## Description
{scene_data.get("description", "Generated with OSSGameForge")}

## How to Play
1. Open index.html in a web browser
2. Use arrow keys to move (if implemented)
3. Enjoy your game!

## Scene Information
- Scene ID: {scene_data.get("id", "unknown")}
- Created: {scene_data.get("created_at", "unknown")}
- Version: {scene_data.get("version", "1.0.0")}

Generated with OSSGameForge
"""
        zip_file.writestr("README.md", readme_content)

    return zip_buffer.getvalue()

@router.post("/export")
async def export_scene(
    request: ExportRequest,
    engine: ExportEngine = Query(default=ExportEngine.HTML5)
):
    """Export scene to playable format"""

    if settings.mock_mode:
        data = load_mock_data()
        scenes = data.get("scenes", [])

        # Find the requested scene
        scene = None
        for s in scenes:
            if s["id"] == request.scene_id:
                scene = s
                break

        if not scene:
            # Try to find in generated scenes (mock)
            # For now, create a default scene
            scene = {
                "id": request.scene_id,
                "name": "Exported Scene",
                "description": "Mock exported scene",
                "version": "1.0.0",
                "metadata": {
                    "width": 1920,
                    "height": 1080,
                    "background_color": "#87CEEB"
                },
                "entities": [
                    {
                        "id": "player",
                        "type": "player",
                        "name": "Player",
                        "position": {"x": 100, "y": 500},
                        "size": {"width": 50, "height": 50},
                        "color": "#FF0000"
                    }
                ],
                "created_at": datetime.utcnow().isoformat() + "Z"
            }

        if engine == ExportEngine.HTML5:
            # Create HTML5 export
            zip_content = create_html5_export(scene)

            return StreamingResponse(
                io.BytesIO(zip_content),
                media_type="application/zip",
                headers={
                    "Content-Disposition": f"attachment; filename=game_export_{scene['id']}.zip"
                }
            )
        elif engine == ExportEngine.GODOT:
            # Mock Godot export (just return a .tscn file content as text)
            tscn_content = f"""[gd_scene format=2]

[node name="Root" type="Node2D"]

[node name="Player" type="KinematicBody2D" parent="."]
position = Vector2({scene['entities'][0]['position']['x']}, {scene['entities'][0]['position']['y']})
"""
            return StreamingResponse(
                io.BytesIO(tscn_content.encode()),
                media_type="text/plain",
                headers={
                    "Content-Disposition": f"attachment; filename=scene_{scene['id']}.tscn"
                }
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Export engine {engine} not yet supported"
            )

    # TODO: Implement real export functionality
    raise HTTPException(status_code=501, detail="Real mode not implemented yet")
