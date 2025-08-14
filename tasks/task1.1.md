### **Task Plan: 1.1 - Project Configuration, CI & Governance (for existing repository)**

**Objective:** To structure the existing `oss-game-forge` repository with a professional, automated foundation. By the end of this task, the cloned repository will be organized locally, the `main` branch on GitHub will be protected by governance rules, and a quality assurance gateway via CI will be active for all future contributions.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** DevOps Lead (1)

---

#### **Phase 1: Local Workspace Setup from Existing Repository**

**Goal:** To create a clean, well-organized local version of the project by cloning the remote repository and then scaffolding the necessary structure within it.

*   **Step 1.1.1: Clone the Existing Repository**
    *   **Action:** Open your terminal or command prompt. Navigate to the directory where you store your development projects. Clone the repository you have already created on GitHub. This will create a local copy of the project named `oss-game-forge` and automatically configure it to track the remote `origin`.
    *   **Command:**
        ```bash
        git clone https://github.com/ClayKa/oss-game-forge.git
        cd oss-game-forge
        ```
    *   **Rationale:** Cloning is the standard procedure for starting work on an existing project. It ensures your local workspace is perfectly synchronized with the remote's initial state.

*   **Step 1.1.2: Scaffold the Core Directory Structure**
    *   **Action:** Inside your now-cloned local repository, create the primary directories that will house the application's different logical parts. This organized structure is crucial for maintainability.
    *   **Command:**
        ```bash
        mkdir -p backend/app frontend/src devops/mocks docs/api_contracts tests/backend
        ```    *   **Rationale:**
        *   `backend/`: For all server-side FastAPI code.
        *   `frontend/`: For all client-side React code.
        *   `devops/`: For Docker configuration and mock data.
        *   `docs/`: For documentation like the API contract.
        *   `tests/`: For all automated tests.

*   **Step 1.1.3: Create Essential Placeholder and Configuration Files**
    *   **Action:** Create the necessary configuration files to define project-specific settings and ensure Git tracks empty directories.
    *   **Commands:**
        ```bash
        # If your README is empty, populate it. If it exists, this will overwrite it.
        echo "# OSSGameForge: The AI-Powered Game Creation Suite" > README.md

        # Create a .gitignore for the backend
        echo "__pycache__/\n*.pyc\n.venv/\n.env" > backend/.gitignore
        
        # Create a .gitignore for the frontend
        echo "node_modules/\ndist/\n.env*" > frontend/.gitignore

        # Create placeholder files so Git tracks the new directories
        touch backend/app/__init__.py tests/backend/__init__.py
        ```
    *   **Rationale:** `.gitignore` files are essential for keeping the repository clean. Placeholder `__init__.py` files are a Python convention and help with module discovery while also ensuring Git tracks the directories.

*   **Step 1.1.4: Commit the New Structure**
    *   **Action:** Stage all the newly created files and directories and commit them. This commit represents the foundational structuring of your project.
    *   **Commands:**
        ```bash
        git add .
        git commit -m "feat: establish core project structure and configuration"
        ```
    *   **Rationale:** This creates a clean historical point in your project that captures the organized directory layout.

---

#### **Phase 2: Pushing Changes & Activating Governance**

**Goal:** To synchronize your local structuring work with the remote repository and then immediately protect the `main` branch.

*   **Step 1.2.1: Push the Structural Commit to GitHub**
    *   **Action:** Push your new commit to the `main` branch on GitHub.
    *   **Command:**
        ```bash
        git push origin main
        ```
    *   **Rationale:** This updates the central repository with the professional structure you've just created, ensuring all team members will have the same layout when they clone or pull.

*   **Step 1.2.2: Configure the Branch Protection Rule**
    *   **Action:** Now that your repository is set up, it's crucial to protect your `main` branch. Navigate to your repository's webpage on GitHub: `https://github.com/ClayKa/oss-game-forge`. Go to `Settings` -> `Branches`. Click `Add branch protection rule`.
    *   **Configuration:**
        1.  In the **"Branch name pattern"** field, type `main`.
        2.  Check the box for **`Require a pull request before merging`**.
        3.  Check the box for **`Require status checks to pass before merging`**.
    *   **Action:** Click the `Create` button to save the rule.
    *   **Rationale:** This rule is the project's most important safety feature. It prevents direct commits to `main` and mandates a review process and passing quality checks for all changes.

---

#### **Phase 3: Quality Assurance Automation**

**Goal:** To define and activate the automated CI pipeline that will serve as the required "status check" for the branch protection rule.

*   **Step 1.3.1: Create a New Branch for CI Implementation**
    *   **Action:** Since `main` is now protected, all new work must be done on a separate branch. Create a new branch for implementing the CI.
    *   **Command:**
        ```bash
        git checkout -b feature/add-ci-pipeline
        ```
    *   **Rationale:** Working on feature branches is a standard best practice that keeps the main branch stable and allows for isolated development and review.

*   **Step 1.3.2: Implement the Continuous Integration (CI) Pipeline**
    *   **Action:** Create the CI workflow file. This YAML file defines the automated jobs.
    *   **File Creation:** Create a new file at the path `.github/workflows/ci.yml`.
    *   **Content:** Add the following configuration:
        ```yaml
        # .github/workflows/ci.yml
        name: Backend CI & Quality Gate
        
        on:
          push:
            branches-ignore: [ main ] # Runs on feature branches
          pull_request:
            branches: [ main ]      # Runs on PRs to main
            
        jobs:
          build_and_test:
            runs-on: ubuntu-latest
            steps:
              - name: Check out repository code
                uses: actions/checkout@v4
              
              - name: Set up Python 3.10
                uses: actions/setup-python@v5
                with:
                  python-version: '3.10'
                  
              - name: Install dependencies
                run: |
                  python -m pip install --upgrade pip
                  pip install ruff pytest
                  
              - name: Lint with Ruff (Static Code Analysis)
                run: ruff check backend
                
              - name: Test with Pytest (Unit Tests)
                run: pytest tests/backend
        ```
    *   **Rationale:** This workflow defines an automated job to check for code style/errors (`Ruff`) and logical correctness (`Pytest`). It will now serve as our quality gate.

*   **Step 1.3.3: Commit and Push the CI Workflow**
    *   **Action:** Commit the new CI workflow file to your feature branch and push it to GitHub.
    *   **Commands:**
        ```bash
        git add .github/workflows/ci.yml
        git commit -m "feat: implement CI pipeline for linting and testing"
        git push -u origin feature/add-ci-pipeline
        ```
    *   **Action:** Go to your repository on GitHub and open a pull request to merge `feature/add-ci-pipeline` into `main`.
    *   **Rationale:** Opening the pull request will trigger the CI workflow for the first time. You can now observe the "Backend CI & Quality Gate" check running, confirming that the entire governance system is active.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of all steps in this task plan, the project will meet the following criteria:

1.  **Repository is Structured and Protected:** The `ClayKa/oss-game-forge` repository contains the new directory structure, and the `main` branch is protected from direct pushes.
2.  **CI is Active:** The "Backend CI & Quality Gate" workflow exists and runs automatically on all pull requests targeting `main`.
3.  **Governance is Enforced:** The branch protection rule is active and will prevent merging any pull request until the CI workflow completes successfully.