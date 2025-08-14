## **OSSGameForge: The Definitive & Competition-Ready Master Plan**

### **Executive Summary & Guiding Principles**

This is the final, definitive blueprint for our hackathon victory. It has been forged through iterative, expert feedback to be resilient, verifiable, and exceptionally easy for judges to evaluate. Our **"Thin, De-risked Slice"** strategy is now fortified with **scalable testing**, **robust CI/CD practices**, and **cross-platform developer experience**. This plan is our commitment to engineering excellence.

#### **Triage: The MUST / SHOULD / WON'T List (Locked and Final)**
Our focus is unwavering. This disciplined focus is our greatest asset.

*   **MUST-HAVE (The Core Loop):**
    *   Asset Upload API with `user_consent` validation & EXIF stripping.
    *   Minimal metadata extraction.
    *   The `generation` API with audit logging and a robust model fallback mechanism.
    *   A frontend "Viewer" that accurately renders the scene JSON.
    *   An `HTML5 Runner` exporter that packages the scene into a universally runnable `.zip` file.
    *   A "Golden Sample" test suite (at least 3 explicitly defined samples) running in CI, with a documented process for expansion.

*   **SHOULD-HAVE (High-Value Enhancements):**
    *   A lightweight playability validator (A* connectivity).
    *   A minimal editor panel to modify an object's position and size.
    *   A text-based `.tscn` (Godot) exporter.

*   **WON'T-HAVE (De-scoped for this Hackathon):**
    *   Full Unity export pipeline.
    *   Interactive timeline editor.
    *   The LoRA fine-tuning pipeline.
    *   The RAG-powered intelligent NPC system.

---

## **Week 1: Foundation & Contracts (Focus: De-risk & Unblock)**

**Goal of the Week:** To establish a rock-solid, simplified foundation. By the end of this week, the CI/CD will be green, and the frontend team will be completely unblocked by a reliable mock API, allowing for maximum parallel development.

### **Task 1.1 (Corrected): Project Init, Version Control & CI**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** DevOps (1)
*   **TODO (Task List):**
    1.  Create the public GitHub repository.
    2.  Make the initial commit to create the `main` branch.
    3.  Push the initial commit to GitHub.
    4.  Configure the branch protection rule for the `main` branch.
    5.  Implement the basic CI pipeline.

*   **Implementation Steps:**
    1.  **Create Repository:** On GitHub, create a new public repository: `oss-game-forge`.
    2.  **Initialize Locally:** Run the following commands:
        ```bash
        git init
        mkdir -p backend/app frontend/src devops/mocks docs/api_contracts
        echo "# OSSGameForge" > README.md
        git add . && git commit -m "feat: initial repository structure"
        ```
    3.  **Push to GitHub:** Connect to the remote and push to create the `main` branch:
        ```bash
        git remote add origin <your-repo-url>
        git branch -M main
        git push -u origin main
        ```
    4.  **Configure Branch Protection:** Now, navigate to repository `Settings` -> `Branches`. Add a protection rule for `main` requiring status checks to pass before merging.
    5.  **Implement CI:** Create `.github/workflows/ci.yml`. Configure it to run `ruff check` and `pytest` on every pull request.

*   **Acceptance Criteria:**
    *   Direct pushes to `main` are blocked.
    *   The CI workflow runs and passes on a new PR.

### **Task 1.2: Simplified Service Orchestration & Mock API First**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Backend (1), Frontend (1)
*   **TODO (Task List):**
    1.  Create a `docker-compose.yml` with only essential services.
    2.  Implement a "mock mode" in the backend to unblock the frontend.
    3.  Define the API contract.

*   **Implementation Steps:**
    1.  Create a `docker-compose.yml` with three services: `postgres`, `minio`, and `backend`.
    2.  **Mock API First:** In the FastAPI app, implement logic controlled by a `MOCK_MODE=true` environment variable. When active, API endpoints will return static JSON from a file, bypassing database/logic calls.
    3.  **API Contract:** In `docs/api_contracts/v1.yaml`, define the schemas for all core endpoints (`POST /assets`, `POST /generate`, etc.) and the structure of the `scene.json`.

*   **Acceptance Criteria:**
    *   Running `docker-compose up` starts the minimal services.
    *   The frontend team can immediately start developing against the backend running in `MOCK_MODE`.

### **Task 1.3: Modular Backend & Minimalist Database**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Backend (1)
*   **TODO (Task List):**
    1.  Design the backend with a modular architecture.
    2.  Define a simplified, focused database schema.

*   **Implementation Steps:**
    1.  **Modular Architecture:** In `backend/app/services/`, create stubs for `context_builder.py`, `inference_client.py`, and `postprocessor.py`.
    2.  **Simplified DB Schema:** In `backend/app/models.py`, define the models:
        *   `Asset`: `id`, `project_id`, `path`, `type`, `status`, `metadata` (JSONB), `consent_hash`, `exif_stripped`.
        *   `GenerationLog`: `id`, `user_id`, `input_hash`, `prompt_hash`, `model_version`, `lora_adapter` (nullable), `status` ('success', 'fail', 'cached'), `latency_ms`, `error` (nullable string), `created_at`.
    3.  **Run Migrations:** Use Alembic to generate and apply migrations.

*   **Acceptance Criteria:**
    *   The three service modules exist as separate files.
    *   The database tables are created with the exact, minimal set of required fields.

---

## **Week 2: The Resilient Core & Scalable Quality Gateway**

**Goal of the Week:** Build the core intelligence pipeline with a heavy focus on resilience and establish a quality gateway that is both robust and explicitly scalable.

### **Task 2.1: Simplified Preprocessing Pipeline**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Backend (1)
*   **TODO (Task List):**
    1.  Implement the upload endpoint with consent check and EXIF stripping.
    2.  Extract only essential metadata using a simple async method.

*   **Implementation Steps:**
    1.  Implement the `POST /projects/{project_id}/assets` endpoint, validating `user_consent: true`.
    2.  **Image Processing:** Use `Pillow` to strip EXIF data before uploading to MinIO.
    3.  **Audio Processing:** Use `tinytag` to extract only basic metadata like `duration`.
    4.  **Async Task Simplification:** Use FastAPI's `BackgroundTasks` for processing to avoid the initial complexity of Celery/Redis.

*   **Acceptance Criteria:**
    *   Uploading an image results in an EXIF-free file in MinIO.
    *   Async processing is handled by `BackgroundTasks` without blocking the API.

### **Task 2.2: The Resilient Generation Engine with Explicit Fallbacks**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Backend (1), ML/Infra (1)
*   **TODO (Task List):**
    1.  Create Golden Samples with a clear coverage strategy and document the extension process.
    2.  Implement the `InferenceClient` with a fallback and document performance expectations.

*   **Implementation Steps:**
    1.  **Golden Samples Strategy:** Create 3 golden sample `.json` files in `backend/app/golden_samples/` to cover:
        *   **Sample 1 (Simple Geometry):** Tests core rendering logic.
        *   **Sample 2 (Asset Intensive):** Tests asset pathing and loading.
        *   **Sample 3 (Complex Structure):** Tests JSON parsing and recursive rendering.
    2.  **Document Extensibility:** In `docs/testing.md`, add a section: **"How to Add New Golden Sample Tests,"** explaining the file placement and naming convention for automatic test discovery.
    3.  **InferenceClient with Fallback:** Implement the `inference_client.py` with the `USE_LOCAL_MODEL` environment variable switch.
    4.  **Document Performance:** In the main `README.md`, add a **"Performance Expectations & Hardware Requirements"** section. State that Fallback Mode is instant, while Local Model Mode requires a GPU with >=16GB VRAM and has an expected latency of 15-45 seconds.
    5.  Implement the API route, logging every call to `GenerationLog`.

*   **Acceptance Criteria:**
    *   The `README.md` contains the new performance expectation section.
    *   The `docs/testing.md` file explains how to add new golden samples.

### **Task 2.3: Golden Sample Test Suite in CI**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** QA (1)
*   **TODO (Task List):**
    1.  Create a test suite validating the generation output schema against the golden samples.
    2.  Integrate this suite into the CI pipeline as a required check.

*   **Implementation Steps:**
    1.  Create `tests/test_generation_pipeline.py`.
    2.  The tests will run with `USE_LOCAL_MODEL=false` and assert that the response from `/generate` matches the expected Pydantic schema.
    3.  Ensure this test runs as part of the `pytest` command in `ci.yml`.

*   **Acceptance Criteria:**
    *   A PR that breaks the structure of the JSON returned by the `/generate` API will cause the CI check to fail.

---

## **Week 3: The Visual Viewer with Consistency & Demo Prep**

**Goal of the Week:** Develop a stable frontend Viewer and begin concrete preparations for the final demo video, ensuring the script is locked and tied to our verifiable golden samples.

### **Task 3.1 & 3.2: Viewer and Minimal Editing**
*   **[Priority]** [MUST] / [SHOULD]
*   **[Suggested Roles]** Frontend (2)
*   **TODO (Task List):**
    1.  Develop the `EditorCanvas` component focused on rendering.
    2.  Implement object selection and highlighting.
    3.  Implement drag-and-drop to update local state.

*   **Implementation Steps:**
    1.  **Canvas as Viewer:** The `EditorCanvas.tsx` will render the scene JSON from the global store using `react-konva`.
    2.  **Selection:** Implement `onClick` handlers to update a `selectedElementId` in the UI store and apply a visual highlight on the canvas.
    3.  **Drag & Drop:** Implement `onDragEnd` to update the object's position in the frontend's Zustand store (local-first update).

*   **Acceptance Criteria:**
    *   Any valid `scene.json` from the backend is rendered correctly.
    *   Users can drag objects, and the position change is reflected in the local state.

### **Task 3.3: Demo Video Scripting Tied to Golden Samples**
*   **[Priority]** [MUST - Risk Management]
*   **[Suggested Roles]** All Team Members (Brainstorm), one Scribe
*   **TODO (Task List):**
    1.  Draft the complete, timed script for the final 3-minute demo video.
    2.  Explicitly tie the script's visuals to a specific golden sample.

*   **Implementation Steps:**
    1.  Create `docs/demo_script.md` with the full narration and a shot list.
    2.  **Explicitly Bind to Sample:** At the top of the script, add a declaration:
        > **Note: This entire demonstration will be recorded using the `golden_sample_platformer.json` test case to ensure a predictable and reproducible result.**

*   **Acceptance Criteria:**
    *   A complete `demo_script.md` file is committed, explicitly stating which golden sample will be used.

---

## **Week 4: Closing the Loop with Verifiable & Robust Demos**

**Goal of the Week:** Achieve the core MVP loop with a new, critical focus: **verifiable consistency**. The CI pipeline will now not only check *if* the demo builds, but *if it runs correctly* in a browser.

### **Task 4.1: The HTML5 Runner Exporter**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Backend (1), Frontend (1)
*   **TODO (Task List):**
    1.  Create a simple, generic HTML5/JavaScript runner template.
    2.  Implement the backend exporter to package the runner, scene data, and assets.

*   **Implementation Steps:**
    1.  **Create Runner:** In `backend/app/runners/html5/`, create an `index.html`, `style.css`, and `runner.js`. The JavaScript will fetch a local `scene.json` and render it to a `<canvas>`.
    2.  **Backend Exporter:** The `POST /export?engine=html5` API will create a `.zip` file containing the runner template, the project's specific `scene.json`, and all required assets from MinIO.

*   **Acceptance Criteria:**
    *   The exported `.zip` can be unzipped, and opening `index.html` in a browser correctly renders the scene.

### **Task 4.2: CI with Robust Browser Smoke Tests**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** QA (1), DevOps (1)
*   **TODO (Task List):**
    1.  Integrate Playwright into the CI pipeline.
    2.  Create a smoke test that validates the exported HTML5 runner *runs*.
    3.  Optimize the CI workflow to manage test duration.

*   **Implementation Steps:**
    1.  **Add Playwright:** `npm install -D @playwright/test`.
    2.  **Create Smoke Test:** Create `tests/e2e/export_runner.spec.ts` to programmatically export a golden sample, unzip it, serve it locally, and use Playwright to launch a headless browser and assert that the `<canvas>` element is visible.
    3.  **CI Optimization:** Modify `ci.yml` to split jobs. Fast unit/lint tests run on every PR. Slower E2E and visual tests run only on merges to `main` or on release tags.
    4.  **Document CI Latency:** In `docs/testing.md`, note that full CI runs may take 2-5 minutes.

*   **Acceptance Criteria:**
    *   The CI pipeline is split into fast (PR) and slow (merge/release) jobs.
    *   A change that breaks the `runner.js` will cause the `e2e_smoke_test` job to fail.

### **Task 4.3: Visual Consistency Check with Tolerance**
*   **[Priority]** [SHOULD]
*   **[Suggested Roles]** QA (1)
*   **TODO (Task List):**
    1.  Implement the pixel-wise comparison test with explicit tolerance and retries.

*   **Implementation Steps:**
    1.  Extend the Playwright test suite to take a screenshot of the viewer canvas and the runner canvas for the same golden sample.
    2.  **Configure Tolerance:** Use `pixelmatch` to compare them with explicit options: `pixelmatch(img1, img2, diff, w, h, { threshold: 0.1 });`.
    3.  **Configure Retries:** In `playwright.config.ts`, enable retries for this test suite: `retries: 1`, to mitigate flakes from minor rendering glitches.

*   **Acceptance Criteria:**
    *   The visual comparison test code includes an explicit tolerance threshold.
    *   The CI configuration for this job includes at least one retry attempt.

### **Task 4.4: The Cross-Platform "One-Click Demo" Script**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** DevOps (1)
*   **TODO (Task List):**
    1.  Create `run_demo.sh` for Linux/macOS and `run_demo.ps1` for Windows.
    2.  Update the README with clear instructions for both platforms.

*   **Implementation Steps:**
    1.  Create `run_demo.sh` to set `USE_LOCAL_MODEL=false` and run `docker-compose up`.
    2.  Create a corresponding `run_demo.ps1` that performs the equivalent actions in PowerShell.
    3.  **Update README:** Create a simple Quick Start section with separate, clear instructions for each platform.

*   **Acceptance Criteria:**
    *   Both scripts exist in the repository.
    *   A non-developer can clone the repo, run a single script on their platform, and see the working app.

---

## **Weeks 5 & 6: Polish, Test, & Deliver**

**Goal of these Weeks:** Feature freeze. The entire focus shifts to stability, reliability, and creating a compelling presentation.

### **Task 5.1: Final Bug Bash & Stability Hardening**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** All Team Members
*   **TODO (Task List):**
    1.  Conduct user testing focused on the core MVP loop.
    2.  Fix all critical bugs found.
    3.  Perform end-to-end regression testing.

*   **Implementation Steps:**
    *   Recruit 3-5 external testers to run through the `Upload -> Generate -> View -> Export -> Run` loop.
    *   Log all bugs and prioritize them. Dedicate 3-4 days exclusively to fixing critical issues.
    *   Continuously run the full CI suite on the `main` branch to ensure no regressions.

*   **Acceptance Criteria:**
    *   All critical bugs that prevent a user from completing the core loop are resolved.

### **Task 5.2: Final Demo Video & Documentation Polish**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** All Team Members, one lead editor
*   **TODO (Task List):**
    1.  Produce the final 3-minute demo video based on the pre-written script.
    2.  Make the `README.md` foolproof for the judges.

*   **Implementation Steps:**
    1.  **Video:** Execute the `demo_script.md` written in Week 3. Record the polished UI and edit the video to be fast-paced and clear.
    2.  **README:** Finalize the README. Ensure the Quick Start is the most prominent section. Add high-quality GIFs.

*   **Acceptance Criteria:**
    *   The final video is under 3 minutes and powerfully demonstrates the working product.
    *   The `README.md` enables a judge to get the project running locally within 15 minutes.

### **Task 5.3: Submission & Celebration**
*   **[Priority]** [MUST]
*   **[Suggested Roles]** Project Lead
*   **TODO (Task List):**
    1.  Triple-check all submission requirements.
    2.  Submit the project with confidence.

*   **Implementation Steps:**
    *   Fill out the submission form, uploading the video and providing the repository link.
    *   Have another team member proofread the entire submission.
    *   Take a screenshot of the confirmation page and celebrate.

*   **Acceptance Criteria:**
    *   The project is submitted on time, and the team is proud of the stable, polished, and impressive product they delivered.