### **Task Plan: 1.2 - Simplified Service Orchestration & Mock API First**

**Objective:** To establish a consistent, reproducible, and simplified development environment using Docker Compose. The primary goal is to stand up only the essential services and immediately provide a "mock" backend API. This unblocks the frontend team from day one, allowing for maximum parallel development without being dependent on the real backend's progress.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** Backend Lead (1), Frontend Lead (1), DevOps (1)

---

#### **Phase 1: Defining the Service Contracts**

**Goal:** To establish a source of truth for how services communicate, before writing significant implementation code.

*   **Step 1.2.1: Define the API Contract**
    *   **Action:** In the `docs/api_contracts/` directory, create a new file named `v1.yaml`. This file will contain the OpenAPI 3.0 specification for our core API endpoints.
    *   **Content:** Define the schemas for the initial MUST-HAVE endpoints. This includes the request body, response codes, and response body structure.
        ```yaml
        # docs/api_contracts/v1.yaml
        openapi: 3.0.0
        info:
          title: OSSGameForge API v1
          version: 1.0.0
        paths:
          /projects/{project_id}/assets:
            post:
              summary: Upload a new asset
              requestBody:
                required: true
                content:
                  multipart/form-data:
                    schema:
                      type: object
                      properties:
                        file:
                          type: string
                          format: binary
                        user_consent:
                          type: boolean
              responses:
                '202':
                  description: Asset upload accepted for processing.
                  content:
                    application/json:
                      schema:
                        type: object
                        properties:
                          asset_id:
                            type: string
                            format: uuid
                          status:
                            type: string
                            example: "processing"
          # ... Define other core endpoints like POST /generate ...
        ```
    *   **Rationale:** This contract acts as a formal agreement between the frontend and backend teams. The frontend can now build components that expect this exact data structure, and the backend knows precisely what it needs to implement.

*   **Step 1.2.2: Create Mock Data Based on the Contract**
    *   **Action:** In the `devops/mocks/` directory, create a `db.json` file. This file will contain static data that mimics the responses defined in your API contract.
    *   **Content:**
        ```json
        {
          "assets": [
            {
              "id": "a1b2c3d4-e5f6-7890-1234-567890abcdef",
              "path": "/assets/sample_image.png",
              "type": "image",
              "status": "processed",
              "metadata": { "tags": ["forest", "night", "adventure"] }
            }
          ],
          "scenes": [
            {
              "id": "s1_golden_sample",
              "description": "A simple platformer level from a golden sample.",
              "entities": [ { "id": "p1", "type": "platform", "x": 100, "y": 200 } ]
            }
          ]
        }
        ```
    *   **Rationale:** This mock data file will be served by our mock API, providing realistic, contract-compliant data for the frontend team to build against immediately.

---

#### **Phase 2: Implementing the Local Development Environment**

**Goal:** To use Docker and Docker Compose to create a single-command startup process for all necessary services.

*   **Step 1.2.3: Define the Backend Dockerfile**
    *   **Action:** In the `backend/` directory, create a file named `Dockerfile`. This file contains the instructions for building a Docker image of our Python backend application.
    *   **Content:**
        ```dockerfile
        # backend/Dockerfile
        FROM python:3.10-slim

        # Set environment variables for better container practices
        ENV PYTHONDONTWRITEBYTECODE 1
        ENV PYTHONUNBUFFERED 1

        # Set the working directory inside the container
        WORKDIR /app

        # Install Python dependencies
        COPY ./requirements.txt /app/requirements.txt
        RUN pip install --no-cache-dir --upgrade pip && pip install --no-cache-dir -r /app/requirements.txt

        # Copy the rest of the application code into the container
        COPY ./backend /app

        # Expose the port the application will run on
        EXPOSE 8000
        
        # The command to run when the container starts
        # --reload is great for development as it restarts the server on code changes
        CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]
        ```
    *   **Action:** Also create a `backend/requirements.txt` file with the initial dependencies:
        ```
        fastapi
        uvicorn[standard]
        sqlalchemy
        psycopg2-binary
        alembic
        python-multipart
        minio
        ```
    *   **Rationale:** The Dockerfile standardizes the backend environment, ensuring it runs the same way on every developer's machine and in CI/CD. The use of `--reload` dramatically improves the development feedback loop.

*   **Step 1.2.4: Create the Docker Compose Configuration**
    *   **Action:** In the project's root directory, create a `docker-compose.yml` file. This file will orchestrate our simplified set of services.
    *   **Content:**
        ```yaml
        # docker-compose.yml
        version: '3.8'

        services:
          # The PostgreSQL Database
          postgres:
            image: postgres:15-alpine
            environment:
              POSTGRES_DB: oss_game_forge_db
              POSTGRES_USER: user
              POSTGRES_PASSWORD: password
            volumes:
              - ./devops/data/postgres:/var/lib/postgresql/data
            ports:
              - "5432:5432"
            networks:
              - gameforge-network

          # The S3-compatible Object Storage for assets
          minio:
            image: minio/minio
            environment:
              MINIO_ROOT_USER: minioadmin
              MINIO_ROOT_PASSWORD: minioadminpassword
            command: server /data --console-address ":9090"
            volumes:
              - ./devops/data/minio:/data
            ports:
              - "9000:9000" # S3 API Port
              - "9090:9090" # Web Console Port
            networks:
              - gameforge-network

          # The Backend Application (with Mock Mode capability)
          backend:
            build:
              context: .
              dockerfile: backend/Dockerfile
            ports:
              - "8000:8000"
            volumes:
              - ./backend:/app # Mount local code for live reloading
            depends_on:
              - postgres
              - minio
            environment:
              DATABASE_URL: "postgresql://user:password@postgres/oss_game_forge_db"
              # Set MOCK_MODE=true to unblock the frontend team
              MOCK_MODE: "true" 
            networks:
              - gameforge-network

        networks:
          gameforge-network:
            driver: bridge
        ```
    *   **Rationale:** This configuration defines our entire development stack in one file. It links services via a shared network, persists data, and mounts local code into the container for instant code changes without rebuilding. The `MOCK_MODE` variable is the key switch to enable parallel development.

---

#### **Phase 3: Verification and Team Handoff**

**Goal:** To ensure the environment works as intended and to officially unblock the frontend team.

*   **Step 1.2.5: Build and Run the Environment**
    *   **Action:** From the project root, run the Docker Compose command to build the images and start all services.
    *   **Command:**
        ```bash
        docker-compose up --build
        ```
    *   **Verification:**
        1.  Check the logs to ensure all containers (`postgres`, `minio`, `backend`) have started without errors.
        2.  Open a web browser and navigate to the MinIO console at `http://localhost:9090` to confirm it's running.
        3.  Use an API client (like Postman, Insomnia, or `curl`) to send a request to the backend's mock endpoint, e.g., `GET http://localhost:8000/projects`. It should immediately return the static JSON data you defined, as per the API contract.

*   **Step 1.2.6: Commit and Document**
    *   **Action:** Commit the new `Dockerfile`, `docker-compose.yml`, `requirements.txt`, and mock data files to your feature branch.
    *   **Documentation:** Update the `README.md` with a new **"Local Development Setup"** section.
        > ### Local Development Setup
        > 1. Ensure you have Docker and Docker Compose installed.
        > 2. Clone the repository.
        > 3. From the project root, run the command:
        >    ```bash
        >    docker-compose up --build
        >    ```
        > 4. The backend API will be available at `http://localhost:8000`. By default, it runs in `MOCK_MODE`, returning static data for frontend development. To switch to the real backend, change the `MOCK_MODE` environment variable in `docker-compose.yml` to `"false"`.
    *   **Rationale:** This finalizes the task by persisting the work and providing clear instructions for all other team members to get started quickly.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Frontend is Unblocked:** The frontend team can start their development immediately by pointing their API calls to `http://localhost:8000`, receiving predictable, contract-compliant mock data.
2.  **Environment is Reproducible:** Any team member can run a single command (`docker-compose up`) to get the exact same minimal development stack running on their machine.
3.  **Contracts are Clear:** The `docs/api_contracts/v1.yaml` file exists as the single source of truth for API communication.
4.  **Backend is Ready for Development:** The backend team has a running application with live-reloading, ready for them to start implementing the real business logic behind the mock endpoints.