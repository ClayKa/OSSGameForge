### **Task Plan: 4.1 - The HTML5 Runner Exporter (Expanded Detail)**

**Objective:** To implement a robust export pipeline that takes a project's state (its `scene.json` and all associated assets) and packages it into a single, self-contained `.zip` file. When unzipped, this package must function as a standalone HTML5 application that can be run in any modern web browser without needing any external dependencies or a web server. This is the ultimate proof that our tool produces a tangible, working artifact.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** Backend Lead (1), with collaboration from a Frontend Engineer (for the runner logic).

---

#### **Phase 1: Creating the Generic HTML5 Runner Template**

**Goal:** To build a simple, reusable set of HTML, CSS, and JavaScript files that can render *any* valid `scene.json` it is provided with. This template is built once and then reused for every export.

*   **Sub-Task 4.1.1: Scaffold the Runner Directory and Files**
    *   **Action:** In the `backend/app/` directory, create a new directory named `runners`. Inside it, create another directory named `html5_template`. This will be the home for our template files.
    *   **Command:**
        ```bash
        mkdir -p backend/app/runners/html5_template
        ```
    *   **Action:** Inside `html5_template`, create the three necessary files.
        ```bash
        touch backend/app/runners/html5_template/index.html
        touch backend/app/runners/html5_template/style.css
        touch backend/app/runners/html5_template/runner.js
        ```
    *   **Rationale:** Isolating the template in its own directory makes the export logic clean and simple. The exporter will just need to copy this entire directory.

*   **Sub-Task 4.1.2: Implement the HTML Structure (`index.html`)**
    *   **Action:** Add the basic HTML boilerplate. The body should contain a single `<canvas>` element, which our JavaScript will target, and a `<script>` tag to load our runner logic.
    *   **Content:**
        ```html
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>OSSGameForge Export</title>
            <link rel="stylesheet" href="style.css">
        </head>
        <body>
            <h1>OSSGameForge Export</h1>
            <canvas id="game-canvas"></canvas>
            <script src="runner.js"></script>
        </body>
        </html>
        ```
    *   **Rationale:** This is the minimal HTML needed to host our application. The `id="game-canvas"` provides a stable hook for our JavaScript to find and draw on.

*   **Sub-Task 4.1.3: Implement the Basic Styling (`style.css`)**
    *   **Action:** Add some simple CSS to center the canvas and give it a border so it's clearly visible.
    *   **Content:**
        ```css
        body { font-family: sans-serif; text-align: center; background-color: #f0f0f0; }
        canvas {
            border: 2px solid #333;
            background-color: #fff;
            margin-top: 20px;
        }
        ```
    *   **Rationale:** Good styling, even if simple, makes the exported result look more professional and polished.

*   **Sub-Task 4.1.4: Implement the JavaScript Runner Logic (`runner.js`)**
    *   **Action:** This is the core of the template. Write the JavaScript code that will load and render the scene. We will use the vanilla Canvas 2D API to avoid external library dependencies, making the runner maximally portable.
    *   **Content:**
        ```javascript
        // runner.js
        document.addEventListener('DOMContentLoaded', () => {
            const canvas = document.getElementById('game-canvas');
            if (!canvas) {
                console.error('Canvas element not found!');
                return;
            }
            const ctx = canvas.getContext('2d');
            canvas.width = 800;
            canvas.height = 600;

            // Main function to start the runner
            async function main() {
                try {
                    // 1. Fetch the scene data
                    const response = await fetch('./scene.json');
                    if (!response.ok) throw new Error('Network response was not ok');
                    const scene = await response.json();

                    // 2. (Optional) Preload assets - advanced, skip for MVP if needed
                    
                    // 3. Render the scene
                    renderScene(scene, ctx);
                } catch (error) {
                    console.error('Failed to load or render scene:', error);
                    ctx.fillStyle = 'red';
                    ctx.fillText('Error loading scene. Check console.', 10, 50);
                }
            }

            function renderScene(scene, context) {
                context.clearRect(0, 0, canvas.width, canvas.height); // Clear canvas
                console.log('Rendering scene:', scene.scene_name);

                // This assumes a simple 'entities' array structure from our golden samples
                if (scene.entities) {
                    scene.entities.forEach(entity => {
                        // For now, we only support simple rectangles
                        if (entity.type === 'platform') {
                            context.fillStyle = 'grey';
                            context.fillRect(entity.x, entity.y, entity.width, entity.height);
                        } else if (entity.type === 'player') {
                            context.fillStyle = 'blue';
                            context.fillRect(entity.x, entity.y, 30, 50);
                        }
                    });
                }
            }
            
            main();
        });
        ```
    *   **Rationale:** This script defines a clear, three-step process: fetch data, (preload assets), and render. By starting with support for only simple shapes, we ensure the core rendering loop works before adding complexity like image loading.

---

#### **Phase 2: Implementing the Backend Export Logic**

**Goal:** To create the API endpoint that orchestrates the packaging of the Runner Template with project-specific content into a downloadable zip file.

*   **Sub-Task 4.1.5: Create the Export Router and Endpoint**
    *   **Action:** In `backend/app/routers/`, create `export.py`. Define the `POST` endpoint that takes a project ID.
    *   **Content:**
        ```python
        # backend/app/routers/export.py
        from fastapi import APIRouter, Depends
        from fastapi.responses import FileResponse
        from sqlalchemy.orm import Session
        from ..database import get_db
        from ..services import export_service # To be created

        router = APIRouter()

        @router.post("/{project_id}/export")
        async def export_project_as_html5(project_id: str, db: Session = Depends(get_db)):
            zip_file_path = export_service.create_html5_package(db, project_id)
            return FileResponse(
                path=zip_file_path, 
                filename=f"oss-game-forge-export-{project_id}.zip",
                media_type="application/zip"
            )
        ```
    *   **Action:** Include this new router in `main.py`.
    *   **Rationale:** This sets up the API layer. The use of `FileResponse` is the standard FastAPI way to stream a file back to the client for download.

*   **Sub-Task 4.1.6: Implement the Export Service**
    *   **Action:** In `backend/app/services/`, create `export_service.py`. This service will contain the core orchestration logic.
    *   **Action:** Import necessary libraries: `os`, `shutil`, `json`, `zipfile`, `pathlib`.
    *   **Content (`export_service.py`):**
        ```python
        # backend/app/services/export_service.py
        import os, shutil, json, zipfile, pathlib, tempfile

        def create_html5_package(db: Session, project_id: str) -> str:
            # 1. Create a temporary directory for packaging
            with tempfile.TemporaryDirectory() as temp_dir:
                temp_path = pathlib.Path(temp_dir)

                # 2. Copy the HTML5 runner template into the temp directory
                runner_template_path = pathlib.Path(__file__).parent.parent / "runners" / "html5_template"
                shutil.copytree(runner_template_path, temp_path, dirs_exist_ok=True)

                # 3. Fetch the project's scene.json data from the DB or another service
                # For this example, we'll use a placeholder
                scene_data = {
                  "scene_name": "My Exported Scene", 
                  "entities": [{"id": "p1", "type": "platform", "x": 50, "y": 400, "width": 150, "height": 20}]
                } 
                
                # 4. Write the project-specific scene.json into the temp directory
                with open(temp_path / "scene.json", "w") as f:
                    json.dump(scene_data, f)
                    
                # 5. Fetch required assets from MinIO and save them to an 'assets' subfolder
                # (This part is a placeholder for now, but the structure is key)
                # os.makedirs(temp_path / "assets")
                # for asset_id in required_assets:
                #     asset_data = storage.download_file(asset_id)
                #     with open(temp_path / "assets" / f"{asset_id}.png", "wb") as f:
                #         f.write(asset_data)

                # 6. Create the final zip archive from the temp directory
                zip_output_path = pathlib.Path(tempfile.gettempdir()) / f"{project_id}.zip"
                with zipfile.ZipFile(zip_output_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for entry in temp_path.rglob('*'):
                        zipf.write(entry, entry.relative_to(temp_path))
                
                return str(zip_output_path)
        ```
    *   **Rationale:** This orchestration is clear and robust. It uses a temporary directory to avoid cluttering the file system. It cleanly separates the steps: copy template, inject data, inject assets, and finally, package.

---

#### **Phase 3: Finalization and Verification**

**Goal:** To commit the working code and verify that the entire export pipeline functions as designed.

*   **Sub-Task 4.1.7: Commit and Test**
    *   **Action:** Commit the new runner template, router, and service files. Restart the Docker environment.
    *   **Manual Verification:**
        1.  Use an API client to send a `POST` request to `http://localhost:8000/projects/test-project-123/export`.
        2.  Verify that the client successfully downloads a `.zip` file.
        3.  Unzip the file.
        4.  Inspect the contents. It must contain `index.html`, `style.css`, `runner.js`, and `scene.json`.
        5.  **The crucial final step:** Double-click the `index.html` file to open it in your local browser (e.g., Chrome, Firefox).
        6.  Verify that the canvas appears and correctly renders the simple platform from the `scene.json` data. Check the browser's developer console for any errors.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Exporter API is Functional:** The `POST /export` endpoint works and returns a `.zip` file.
2.  **Package is Self-Contained:** The downloaded `.zip` file contains all necessary files (`html`, `css`, `js`, `json`) to run independently.
3.  **Runner is Universally Runnable:** The `index.html` file from the unzipped package can be opened directly in a standard web browser and successfully executes, rendering the scene without requiring a web server or any other dependencies.
4.  **Logic is Separated:** The generic Runner Template code is cleanly separated from the backend's dynamic packaging logic, making both easy to maintain.