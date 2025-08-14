### **Task Plan: 2.3 - Golden Sample Test Suite in CI (Expanded Detail)**

**Objective:** To create an automated, reliable test suite that verifies the end-to-end integrity of our content generation pipeline. This suite will act as a critical quality gate, running automatically in our Continuous Integration (CI) environment to prevent any code change from accidentally breaking the structure of our core data output.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** QA Lead (1), Backend Engineer (1)

---

#### **Phase 1: Structuring the Test Environment**

**Goal:** To prepare the necessary files and configurations to write and run integration tests using Pytest and to interact with our FastAPI application within a testing context.

*   **Sub-Task 2.3.1: Set up the Pytest Test Client**
    *   **Step 1:** Ensure `pytest` and a suitable HTTP client library are listed in your `backend/requirements-dev.txt` (it's good practice to separate dev dependencies).
        ```
        # backend/requirements-dev.txt
        pytest
        httpx # A modern, async-capable HTTP client
        ```
    *   **Step 2:** In the `tests/` directory, create a `conftest.py` file. This is a special Pytest file used for providing fixtures (reusable setup/teardown code) to all tests.
    *   **Step 3:** In `tests/conftest.py`, create a fixture that provides an `httpx` client capable of making requests to our FastAPI application.
        ```python
        # tests/conftest.py
        import pytest
        from fastapi.testclient import TestClient
        from backend.app.main import app # Import our main FastAPI app

        @pytest.fixture(scope="module")
        def client():
            """
            Provides a TestClient instance for making API requests in tests.
            """
            with TestClient(app) as c:
                yield c
        ```
    *   **Rationale:** The `TestClient` from FastAPI is specifically designed for testing. It runs the application in-memory, making tests extremely fast and self-contained, without needing a live running server. The fixture makes this client available to any test function simply by adding it as an argument.

*   **Sub-Task 2.3.2: Create the Test File and Pydantic Validation Models**
    *   **Step 1:** In the `tests/backend/` directory, create the test file `test_generation_pipeline.py`.
    *   **Step 2:** To validate the JSON response, we will need Pydantic models that define the expected structure. While our main app might have these, it's good practice to define explicit validation schemas for testing. In a new file, `tests/schemas/scene.py`, define the expected output structure.
        ```python
        # tests/schemas/scene.py
        from pydantic import BaseModel, Field
        from typing import List, Optional

        class Entity(BaseModel):
            id: str
            type: str
            x: int
            y: int
            # Add other optional fields as needed

        class Scene(BaseModel):
            scene_name: str
            entities: Optional[List[Entity]] = Field(default_factory=list)
            layers: Optional[List[dict]] = Field(default_factory=list) # Simplified for testing
        ```
    *   **Rationale:** Using Pydantic models for validation is far more robust and readable than manually checking for keys in a dictionary. It ensures not only that keys exist but also that their values have the correct data type.

---

#### **Phase 2: Writing the Integration Tests**

**Goal:** To implement the actual test cases that call our API and validate the responses.

*   **Sub-Task 2.3.3: Write the Core Generation Test**
    *   **Step 1:** Open `tests/backend/test_generation_pipeline.py`. Import `TestClient` from FastAPI, `pytest`, and your new `Scene` validation schema.
    *   **Step 2:** Write a test function named `test_generate_endpoint_in_fallback_mode`. This function will take the `client` fixture as an argument.
    *   **Step 3:** **Set the Environment:** Inside the test, use `monkeypatch` (a Pytest fixture) to reliably set the `USE_LOCAL_MODEL` environment variable to `"false"` for the duration of this single test. This ensures the test is deterministic and always uses the fallback mechanism.
    *   **Step 4:** **Make the API Call:** Use the `client` to make a `POST` request to the `/generate` endpoint. Provide a minimal, valid request body.
    *   **Step 5:** **Perform Assertions:**
        *   Assert that the HTTP response status code is `200 OK`.
        *   Parse the JSON response body.
        *   Use a `try-except` block to attempt to validate the response data against your `Scene` Pydantic model. If it fails, the test should fail with a clear error message.
        ```python
        # tests/backend/test_generation_pipeline.py
        from fastapi.testclient import TestClient
        from ..schemas.scene import Scene # Import our validation schema
        import pytest

        def test_generate_endpoint_in_fallback_mode(client: TestClient, monkeypatch):
            """
            GIVEN the application is in fallback mode
            WHEN a request is made to the /generate endpoint
            THEN it should return a successful response
            AND the response body should conform to the Scene schema
            """
            # 1. ARRANGE: Set the environment to force fallback mode
            monkeypatch.setenv("USE_LOCAL_MODEL", "false")
            
            # A minimal valid request body
            request_data = {"prompt": "Generate a simple level"}

            # 2. ACT: Make the API call
            response = client.post("/generate", json=request_data)

            # 3. ASSERT: Check the outcomes
            # Assert HTTP success
            assert response.status_code == 200, f"Expected 200 OK, got {response.status_code}"

            # Assert the response is valid JSON
            response_data = response.json()
            
            # Assert the JSON structure conforms to our Pydantic model
            try:
                Scene.parse_obj(response_data)
            except Exception as e:
                pytest.fail(f"Response JSON does not match Scene schema. Error: {e}")
        ```
    *   **Rationale:** This test provides a complete end-to-end check of the "happy path" for our most critical feature in its safest mode. It validates the HTTP layer, the JSON serialization, and the data structure itself.

---

#### **Phase 3: Integrating the Test Suite into the CI Pipeline**

**Goal:** To ensure these critical tests are run automatically on every proposed code change, acting as our project's quality gate.

*   **Sub-Task 2.3.4: Verify Pytest Configuration**
    *   **Step 1:** At the root of your project, create a `pytest.ini` or `pyproject.toml` file to configure Pytest. This helps Pytest discover your tests correctly.
    *   **Content (`pytest.ini`):**
        ```ini
        [pytest]
        pythonpath = .
        ```
    *   **Rationale:** This tells Pytest to add the project root to the Python path, ensuring that imports like `from backend.app.main import app` work correctly when running tests from the command line or in CI.

*   **Sub-Task 2.3.5: Update the CI Workflow File**
    *   **Step 1:** Open `.github/workflows/ci.yml`.
    *   **Step 2:** Locate the `Test with Pytest` step within the `build_and_test` job.
    *   **Step 3:** Ensure the command is simply `pytest`. Pytest will automatically discover and run all files named `test_*.py` or `*_test.py`.
        ```yaml
        # In .github/workflows/ci.yml
        # ...
              - name: Test with Pytest (Unit & Integration Tests)
                run: pytest
        ```
    *   **Action:** Commit and push these changes (`test_generation_pipeline.py`, `tests/schemas/scene.py`, `pytest.ini`) in a new pull request.
    *   **Verification:** When the pull request is opened, observe the "Backend CI & Quality Gate" check. It should now run for a slightly longer duration as it executes our new integration test. Verify that it passes.

*   **Sub-Task 2.3.6: Test the Failure Case**
    *   **Action (optional but recommended):** To be absolutely sure the quality gate works, intentionally introduce a breaking change. For example, change a key in one of the `golden_samples` files from `"scene_name"` to `"name"`.
    *   **Action:** Commit this change to your feature branch and push it.
    *   **Verification:** The CI job should now **fail**. The logs for the "Test with Pytest" step should clearly show a Pydantic validation error, proving that your quality gate has successfully caught a regression. Revert the change to make the test pass again.
    *   **Rationale:** Actively testing your test suite's ability to fail is a hallmark of a mature engineering process. It builds confidence that the safety net is actually working.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Test Suite Exists:** The file `tests/backend/test_generation_pipeline.py` exists and contains a test that validates the `/generate` endpoint's response schema.
2.  **CI Integration is Active:** The `ci.yml` workflow is configured to execute this test suite on every pull request to `main`.
3.  **Quality Gate is Functional:** A pull request containing a code change that breaks the structure of the JSON returned by the `/generate` API will cause the "Backend CI & Quality Gate" check to fail, thus preventing the faulty code from being merged.