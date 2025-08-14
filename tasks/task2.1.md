### **Task Plan: 2.1 - Simplified Preprocessing Pipeline (Expanded Detail)**

**Objective:** To implement a secure and efficient asset ingestion pipeline. This task covers the creation of the API endpoint for file uploads, enforcement of user consent, sanitization of image metadata, and extraction of only the most essential asset information using a lightweight asynchronous process. This is the official entry point for user content into our system.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** Backend Engineer (2)

---

#### **Phase 1: API Endpoint and Security/Compliance Gateway**

**Goal:** To create the public-facing API endpoint and build in the mandatory security and compliance checks from the very start.

*   **Sub-Task 2.1.1: Create the Asset Router and Endpoint**
    *   **Step 1:** In the `backend/app/routers/` directory, create a new file named `assets.py`.
    *   **Step 2:** Inside `assets.py`, import the necessary FastAPI and dependency modules.
        ```python
        from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException, status, BackgroundTasks
        from sqlalchemy.orm import Session
        import uuid
        from ..database import get_db
        from ..services import asset_service
        ```
    *   **Step 3:** Define the router instance.
        ```python
        router = APIRouter()
        ```
    *   **Step 4:** Define the `upload_asset` function signature, specifying its route (`/`), method (`POST`), and expected status code (`202 Accepted`). Use dependency injection for `BackgroundTasks` and `db: Session`.
        ```python
        @router.post("/", status_code=status.HTTP_202_ACCEPTED)
        async def upload_asset(
            background_tasks: BackgroundTasks,
            db: Session = Depends(get_db),
            project_id: str = Form(...),
            user_consent: bool = Form(...),
            file: UploadFile = File(...)
        ):
            # Function body will be added in subsequent steps
            pass
        ```
    *   **Step 5:** Open `backend/app/main.py`. Import the newly created assets router and include it in the main FastAPI app instance with a prefix and tag.
        ```python
        # In backend/app/main.py
        from .routers import health, assets # Add 'assets'
        # ...
        app.include_router(assets.router, prefix="/assets", tags=["Assets"])
        ```
    *   **Rationale:** This establishes the structured, organized endpoint. Defining the full function signature with dependencies makes the API's requirements explicit and leverages FastAPI's powerful framework features.

*   **Sub-Task 2.1.2: Implement the User Consent Gateway**
    *   **Step 1:** Inside the `upload_asset` function in `assets.py`, add a conditional check at the very beginning of the function body.
    *   **Step 2:** The condition will check if the `user_consent` form field is not `True`.
    *   **Step 3:** If the condition is met, raise an `HTTPException` with a `400 Bad Request` status code and a clear, user-facing error message.
        ```python
        # First lines inside the upload_asset function
        if not user_consent:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="User consent is mandatory and must be explicitly set to 'true'."
            )
        ```
    *   **Rationale:** This is the project's primary compliance gate. By placing it first, we ensure no system resources are used or data is processed without explicit user permission, minimizing risk.

*   **Sub-Task 2.1.3: Create an Asset Service and Initial Database Record**
    *   **Step 1:** In `backend/app/services/`, create a new file named `asset_service.py`.
    *   **Step 2:** Inside `asset_service.py`, create the `create_initial_asset_record` function. This function will encapsulate the logic for creating and saving a new `Asset` model instance.
        ```python
        # backend/app/services/asset_service.py
        from sqlalchemy.orm import Session
        import hashlib
        import time
        from .. import models
        from ..database import SessionLocal # Import SessionLocal for background tasks

        def create_initial_asset_record(db: Session, project_id: str, filename: str, content_type: str) -> models.Asset:
            user_id = "user_placeholder_123" # Placeholder for now
            
            # Create a unique hash for consent tracking
            consent_hash = hashlib.sha256(f"{user_id}{filename}{time.time()}".encode()).hexdigest()

            # Create the SQLAlchemy model instance
            new_asset = models.Asset(
                project_id=project_id,
                path="pending", # Temporary placeholder path
                type=content_type, # Store the MIME type
                consent_hash=consent_hash
            )
            
            # Add to session, commit, and refresh to get the generated ID
            db.add(new_asset)
            db.commit()
            db.refresh(new_asset)
            return new_asset
        ```
    *   **Step 3:** Back in `assets.py`, inside the `upload_asset` function (after the consent check), call this new service function to create the database entry.
        ```python
        # Inside upload_asset function
        new_asset = asset_service.create_initial_asset_record(
            db=db, 
            project_id=project_id, 
            filename=file.filename,
            content_type=file.content_type
        )
        ```
    *   **Rationale:** This step separates concerns. The router handles HTTP, and the service handles business logic. Creating the DB record early provides a stable, unique ID (`new_asset.id`) that we can use for all subsequent operations like naming the file in storage.

---

#### **Phase 2: File Handling and Lightweight Asynchronous Processing**

**Goal:** To securely store the uploaded file and then trigger a non-blocking, simple background task to perform the minimal required metadata extraction.

*   **Sub-Task 2.1.4: Implement Secure File Storage to MinIO**
    *   **Step 1:** Create `backend/app/storage.py` to manage the MinIO client.
        ```python
        # backend/app/storage.py
        from minio import Minio
        # ... client initialization using environment variables ...
        minio_client = Minio(...)
        
        def upload_file_to_storage(bucket_name: str, object_name: str, data, length: int, content_type: str):
            minio_client.put_object(bucket_name, object_name, data, length, content_type)
        ```    *   **Step 2:** In `asset_service.py`, create a new function `process_and_store_file`.
    *   **Step 3:** This function will determine the final object name for storage, e.g., `{project_id}/{asset_id}/{original_filename}`.
    *   **Step 4:** **[Image Processing & EXIF Strip]** Inside this function, check the asset's `type` (`content_type`). If it's an image (`image/jpeg`, `image/png`, etc.):
        *   Import `PIL` and `io`.
        *   Use `Image.open(file.file)` to read the uploaded file data.
        *   Create a new image from the pixel data to discard the metadata: `image_without_exif = Image.new(image.mode, image.size); image_without_exif.putdata(list(image.getdata()))`.
        *   Save this sanitized image to an in-memory `io.BytesIO` buffer.
        *   Call `storage.upload_file_to_storage` with this buffer's data.
        *   Update the database record: `asset.exif_stripped = True`.
    *   **Step 5:** If the file is not an image, simply pass the original `file.file` object to the `storage.upload_file_to_storage` function.
    *   **Step 6:** After a successful upload, update the asset's `path` in the database with the final object name and commit the change.
    *   **Step 7:** Call this new `process_and_store_file` function from the `upload_asset` router.
    *   **Rationale:** This detailed flow ensures that image sanitization is an integral, non-skippable part of the storage process. It handles different file types correctly and updates the database with the final, correct storage path.

*   **Sub-Task 2.1.5: Trigger Simplified Background Processing**
    *   **Step 1:** In the `assets.py` router, after the file has been successfully stored and the DB record updated, add the call to `background_tasks.add_task`.
        ```python
        # At the end of the upload_asset function
        background_tasks.add_task(asset_service.extract_metadata_task, asset_id=new_asset.id)
        
        return {"asset_id": str(new_asset.id), "status": "processing"}
        ```
    *   **Step 2:** In `asset_service.py`, create the `extract_metadata_task` function. This function MUST handle its own database session because it runs in a separate thread after the original request's session has closed.
        ```python
        def extract_metadata_task(asset_id: uuid.UUID):
            # Each background task needs its own DB session
            db = SessionLocal()
            try:
                asset = db.query(models.Asset).filter(models.Asset.id == asset_id).first()
                if not asset:
                    return # Or log an error
                
                # ... Download file from MinIO to a temporary file/buffer ...
                # (You will need a download function in storage.py)
                
                # [Audio Processing]
                if asset.type.startswith("audio/"):
                    import tinytag
                    try:
                        tag = tinytag.TinyTag.get(temp_file_path)
                        asset.metadata = {"duration_seconds": tag.duration, "samplerate": tag.samplerate, "bitrate": tag.bitrate}
                    except Exception as e:
                        asset.status = "error_processing"
                        asset.metadata = {"error": str(e)}

                # Add other minimal processing if needed
                
                if asset.status != "error_processing":
                    asset.status = "processed"

                db.commit()
            finally:
                db.close()
        ```
    *   **Rationale:** This structure is robust. It correctly manages database sessions in a background context. It also includes basic error handling, so if `tinytag` fails on a corrupt file, the asset's status is updated to `error_processing` instead of crashing the worker. The API returns instantly, providing a responsive user experience.

---

#### **Phase 3: Finalization and Verification**

**Goal:** To commit the working code and verify that the entire pipeline functions as designed through targeted testing.

*   **Sub-Task 2.1.6: Commit and Test**
    *   **Step 1:** Commit all new and modified files (`assets.py`, `asset_service.py`, `storage.py`, `models.py`) to your feature branch.
    *   **Step 2:** Restart the Docker environment: `docker-compose up --build -d`.
    *   **Step 3:** Use an API client to perform the following tests:
        *   **Test Case 1 (Consent Failure):** `POST /assets` with `user_consent=false`. **Expected:** `400 Bad Request`.
        *   **Test Case 2 (Image Success):** `POST /assets` with a JPG/PNG image file and `user_consent=true`. **Expected:** `202 Accepted`.
        *   **Test Case 3 (Audio Success):** `POST /assets` with an MP3 file and `user_consent=true`. **Expected:** `202 Accepted`.
    *   **Step 4:** **Verify Image Processing:** Download the image file directly from the MinIO console. Use an online EXIF viewer or a local tool to confirm it contains no metadata. Check the `assets` table to see `exif_stripped` is `true`.
    *   **Step 5:** **Verify Audio Processing:** After a few seconds, query the `assets` table for the audio file's record. Check that the `metadata` column contains a JSON object with `duration_seconds` and `samplerate`, and the `status` is `processed`.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Endpoint is Live and Secure:** The `POST /assets` endpoint is functional and correctly rejects requests without consent.
2.  **Files are Sanitized and Stored:** Image files are verifiably stripped of EXIF data before being stored in MinIO. All files are stored under a structured path.
3.  **Database is Atomically Updated:** The asset's record is updated throughout the process (path, status, metadata) in a transactional and safe manner.
4.  **Process is Asynchronous and Robust:** The API responds instantly. Metadata extraction happens in the background, and the process includes basic error handling for corrupt files.
5.  **Scope is Contained:** The implementation has strictly adhered to the MVP requirements, successfully avoiding feature creep by not implementing complex ML-based tagging or beat detection.