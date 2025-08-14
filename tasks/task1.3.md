### **Task Plan: 1.3 - Modular Backend & Minimalist Database**

**Objective:** To implement the foundational code for our FastAPI backend, including a modular service architecture and the core database models. This task transitions us from a "mock" API to a real, albeit empty, application structure that is ready for business logic implementation. It establishes the "source of truth" for our data within the PostgreSQL database.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** Backend Lead (1), Backend Engineer (1)

---

#### **Phase 1: Structuring the FastAPI Application**

**Goal:** To create a well-organized file and module structure for the FastAPI application that promotes separation of concerns.

*   **Step 1.3.1: Create the Main Application Entrypoint**
    *   **Action:** In the `backend/app/` directory, create a file named `main.py`. This will be the main entry point for our application, where the FastAPI instance is created and routers are included.
    *   **Content:**
        ```python
        # backend/app/main.py
        from fastapi import FastAPI
        from .routers import health # We will create this next

        app = FastAPI(
            title="OSSGameForge API",
            description="The backend service for the AI-Powered Game Creation Suite.",
            version="1.0.0"
        )

        # Include routers for different parts of the application
        app.include_router(health.router, prefix="/health", tags=["Health"])

        @app.get("/", tags=["Root"])
        async def read_root():
            return {"message": "Welcome to the OSSGameForge API"}
        ```
    *   **Rationale:** This establishes a clean entry point. Using routers allows us to keep different logical parts of our API (like health checks, user management, project management) in separate files, preventing `main.py` from becoming bloated.

*   **Step 1.3.2: Implement a Health Check Endpoint**
    *   **Action:** In the `backend/app/routers/` directory, create a file named `health.py`. This router will contain a simple endpoint to verify that the application is running and can connect to its dependencies.
    *   **Content:**
        ```python
        # backend/app/routers/health.py
        from fastapi import APIRouter, Depends
        from sqlalchemy.orm import Session
        from ..database import get_db # We will create this next

        router = APIRouter()

        @router.get("/")
        async def check_health(db: Session = Depends(get_db)):
            try:
                # A simple query to check DB connectivity
                db.execute('SELECT 1')
                db_status = "ok"
            except Exception:
                db_status = "error"
            
            return {
                "status": "ok",
                "services": {
                    "database": db_status
                }
            }
        ```
    *   **Rationale:** A health check endpoint is a best practice. It provides a simple way for developers and automated systems (like a load balancer in the future) to verify the service's operational status.

*   **Step 1.3.3: Configure the Database Connection**
    *   **Action:** In the `backend/app/` directory, create `database.py`. This module will handle creating the SQLAlchemy engine and managing database sessions.
    *   **Content:**
        ```python
        # backend/app/database.py
        import os
        from sqlalchemy import create_engine
        from sqlalchemy.ext.declarative import declarative_base
        from sqlalchemy.orm import sessionmaker

        DATABASE_URL = os.getenv("DATABASE_URL")

        engine = create_engine(DATABASE_URL)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        Base = declarative_base()

        # Dependency to be used in API routes
        def get_db():
            db = SessionLocal()
            try:
                yield db
            finally:
                db.close()
        ```
    *   **Rationale:** Centralizing database connection logic makes it easy to manage and configure. The `get_db` dependency injector is a standard FastAPI pattern for safely providing and closing database sessions for each API request.

---

#### **Phase 2: Defining the Data "Schema"**

**Goal:** To translate our project's data requirements into concrete database tables using SQLAlchemy ORM and to set up a migration system to manage schema changes over time.

*   **Step 1.3.4: Implement the SQLAlchemy Models**
    *   **Action:** In the `backend/app/models/` directory, create a file named `core_models.py` (or similar). This file will define our database tables as Python classes, inheriting from the `Base` object we created in `database.py`.
    *   **Content:**
        ```python
        # backend/app/models/core_models.py
        from sqlalchemy import Column, Integer, String, Boolean, DateTime, JSON, ForeignKey
        from sqlalchemy.orm import relationship
        from sqlalchemy.dialects.postgresql import UUID
        import uuid
        from datetime import datetime
        from ..database import Base

        class Asset(Base):
            __tablename__ = "assets"
            id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            project_id = Column(String, nullable=False) # Simplified for now
            path = Column(String, nullable=False)
            type = Column(String, nullable=False)
            status = Column(String, nullable=False, default='uploaded')
            metadata = Column(JSON)
            consent_hash = Column(String, nullable=False)
            exif_stripped = Column(Boolean, default=False)
            created_at = Column(DateTime, default=datetime.utcnow)

        class GenerationLog(Base):
            __tablename__ = "generation_logs"
            id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
            user_id = Column(String, nullable=False) # Simplified for now
            input_hash = Column(String, nullable=False)
            prompt_hash = Column(String, nullable=False)
            model_version = Column(String, nullable=False)
            lora_adapter = Column(String, nullable=True)
            status = Column(String, nullable=False) # 'success', 'fail', 'cached'
            latency_ms = Column(Integer)
            error = Column(String, nullable=True)
            created_at = Column(DateTime, default=datetime.utcnow)
        ```
    *   **Rationale:** This code is the "source of truth" for our database structure. Using an ORM like SQLAlchemy allows us to work with Python objects instead of raw SQL, reducing errors and improving maintainability. We are defining exactly the minimal fields required by the revised plan.

*   **Step 1.3.5: Set Up Alembic for Database Migrations**
    *   **Action:** Initialize and configure Alembic to manage changes to our database schema. This is a critical step for collaborative and production environments.
    *   **Commands (run from inside the running `backend` container):**
        ```bash
        # 1. Access the running container's shell
        docker-compose exec backend bash

        # 2. Install alembic if not already in requirements.txt
        pip install alembic

        # 3. Initialize the alembic environment
        alembic init alembic
        ```
    *   **Configuration:**
        1.  **Edit `alembic.ini`:** Find the line `sqlalchemy.url = ...` and change it to read from our environment variable: `sqlalchemy.url = %(DATABASE_URL)s`.
        2.  **Edit `alembic/env.py`:** At the top of the file, import your models' `Base` object and set the `target_metadata` variable.
            ```python
            # alembic/env.py
            from app.database import Base # Adjust path as necessary
            # ... other imports ...
            target_metadata = Base.metadata
            ```
    *   **Rationale:** Manually managing database schema changes is error-prone. Alembic automates this process by comparing your SQLAlchemy models to the current database state and generating SQL migration scripts.

*   **Step 1.3.6: Generate and Apply the Initial Migration**
    *   **Action:** Use Alembic to generate the first migration script based on your new models, and then apply it to the database to create the tables.
    *   **Commands (run from inside the `backend` container's shell):**
        ```bash
        # 1. Generate the migration script. The message describes the change.
        alembic revision --autogenerate -m "Create initial Asset and GenerationLog tables"

        # 2. Apply the migration script to the database.
        alembic upgrade head
        ```
    *   **Verification:**
        1.  Connect to your PostgreSQL database (e.g., using `psql` inside the container or a GUI client like DBeaver on `localhost:5432`).
        2.  Verify that the `assets` and `generation_logs` tables now exist and have the exact columns defined in your models.

---

#### **Phase 3: Final Integration and Verification**

**Goal:** To ensure the entire application stack is working together correctly after implementing the real backend structure.

*   **Step 1.3.7: Commit and Restart Services**
    *   **Action:** Exit the container's shell. Commit all the new backend files (`main.py`, `database.py`, models, alembic migrations) to your feature branch. Then, restart your Docker services to ensure everything loads correctly with the new code.
    *   **Command:**
        ```bash
        # Press Ctrl+C to stop the running services, then:
        docker-compose up --build
        ```
*   **Step 1.3.8: Test the Live Application**
    *   **Action:** With the services running again, test the live (non-mocked) application.
    *   **Verification:**
        1.  Change the `MOCK_MODE` environment variable in `docker-compose.yml` to `"false"`.
        2.  Restart the services: `docker-compose up -d`.
        3.  Send a `GET` request to the health check endpoint: `http://localhost:8000/health`. The response should now show `"database": "ok"`. This confirms your FastAPI application is successfully connecting to the PostgreSQL database inside Docker.
        4.  Change `MOCK_MODE` back to `"true"` so the frontend team remains unblocked.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Modular Structure is in Place:** The `backend/app` directory is organized into `routers`, `services`, `models`, etc., establishing a clean architecture.
2.  **Database is Live and Managed:** The PostgreSQL database is running, and the `assets` and `generation_logs` tables have been created and are now managed by Alembic.
3.  **Application Connects to Database:** The FastAPI application can successfully establish a connection to the database, as proven by the live health check endpoint.
4.  **Ready for Logic Implementation:** The backend is no longer just a mock. It is a fully structured application ready for the team to start implementing the business logic for the asset upload and generation endpoints in the subsequent tasks.