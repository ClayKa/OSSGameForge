### **Task Plan: 4.4 - The Cross-Platform "One-Click Demo" Script (Expanded Detail)**

**Objective:** To create a set of simple, executable scripts that automate the entire local setup and launch process for a demonstration. This will provide an exceptional "first run" experience, allowing anyone (especially judges) to clone the repository and see a working demo in their browser within minutes, with zero configuration required. This task directly addresses the key success metric of "reproducibility."

**[Priority]** [MUST]
**[Owner / Suggested Roles]** DevOps Lead (1)

---

#### **Phase 1: Implementing the Script for Linux and macOS**

**Goal:** To create a robust `bash` script that works reliably on standard Unix-like operating systems.

*   **Sub-Task 4.4.1: Create the `run_demo.sh` File**
    *   **Action:** In the root directory of the project, create a new file named `run_demo.sh`.
    *   **Command:**
        ```bash
        touch run_demo.sh
        ```

*   **Sub-Task 4.4.2: Write the Bash Script Logic**
    *   **Action:** Add the script logic to `run_demo.sh`. The script will be designed to be informative, showing the user what it's doing at each step.
    *   **Content:**
        ```bash
        #!/bin/bash
        
        # Add a "shebang" to ensure the script is run with bash.
        # Use 'set -e' to make the script exit immediately if any command fails.
        set -e
        
        echo "--- 🚀 Starting OSSGameForge Demo Environment ---"
        echo "This script will build and start all necessary services using Docker Compose."
        echo "The application will run in 'Fallback Mode', serving pre-made golden samples."
        
        # Step 1: Check for Docker installation
        if ! command -v docker &> /dev/null
        then
            echo "❌ Error: Docker is not installed. Please install Docker before running this script."
            exit 1
        fi
        
        # Step 2: Set the environment variable to ensure we use fallback mode
        # This exports the variable for the scope of this script and its child processes.
        export USE_LOCAL_MODEL=false
        
        # Step 3: Build and start the services in detached mode (-d)
        echo ""
        echo "--- Building Docker images and starting services... (This may take a few minutes on the first run) ---"
        docker-compose up --build -d
        
        # Step 4: Provide clear, actionable information to the user
        echo ""
        echo "--- ✅ Success! Services are running. ---"
        echo ""
        echo "   - Frontend Viewer is available at: http://localhost:5173"
        echo "   - Backend API is available at:      http://localhost:8000"
        echo "   - MinIO Storage Console at:       http://localhost:9090"
        echo ""
        echo "--- Tailing logs (Press Ctrl+C to stop everything) ---"
        
        # Step 5: Attach to the logs so the user can see activity.
        # This also keeps the script running, so Ctrl+C will trigger the shutdown trap.
        docker-compose logs -f
        ```

*   **Sub-Task 4.4.3: Add a Graceful Shutdown Mechanism**
    *   **Action:** Add a "trap" to the script. This is a mechanism in bash that catches signals, like the user pressing `Ctrl+C`, and allows us to run a cleanup command before the script exits.
    *   **Content (add at the top of `run_demo.sh`):**
        ```bash
        # Trap the EXIT signal to run a cleanup function
        cleanup() {
            echo ""
            echo "---  shutting down services... ---"
            docker-compose down
            echo "--- ✅ Environment stopped. ---"
        }
        trap cleanup EXIT
        ```
    *   **Rationale:** This makes the script much more user-friendly. When the user is done, they can simply press `Ctrl+C`, and the script will automatically stop and remove the Docker containers, leaving their system clean.

*   **Sub-Task 4.4.4: Make the Script Executable**
    *   **Action:** Change the file permissions on the script to make it executable.
    *   **Command:**
        ```bash
        chmod +x run_demo.sh
        ```
    *   **Rationale:** Without this permission, users would have to run `bash run_demo.sh`. With it, they can use the simpler, standard `./run_demo.sh`.

---

#### **Phase 2: Implementing the Script for Windows**

**Goal:** To provide an equivalent, native experience for users on Windows using PowerShell.

*   **Sub-Task 4.4.5: Create the `run_demo.ps1` File**
    *   **Action:** In the root directory of the project, create a new file named `run_demo.ps1`.

*   **Sub-Task 4.4.6: Write the PowerShell Script Logic**
    *   **Action:** Add the PowerShell script logic. The logic mirrors the bash script but uses PowerShell syntax.
    *   **Content:**
        ```powershell
        # Set strict mode to catch errors
        Set-StrictMode -Version Latest
        
        # Trap Ctrl+C for graceful shutdown
        $trap_block = {
            Write-Host ""
            Write-Host "--- shutting down services... ---" -ForegroundColor Yellow
            docker-compose down
            Write-Host "--- ✅ Environment stopped. ---" -ForegroundColor Green
            # Exit the script
            exit 0
        }
        trap { $trap_block.Invoke() }

        Write-Host "--- 🚀 Starting OSSGameForge Demo Environment (Windows) ---" -ForegroundColor Cyan
        Write-Host "This script will build and start all necessary services using Docker Compose."
        Write-Host "The application will run in 'Fallback Mode', serving pre-made golden samples."

        # Step 1: Check for Docker installation
        if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
            Write-Host "❌ Error: Docker is not installed. Please install Docker Desktop before running this script." -ForegroundColor Red
            exit 1
        }
        
        # Step 2: Set the environment variable for fallback mode
        $env:USE_LOCAL_MODEL = "false"
        
        # Step 3: Build and start services
        Write-Host ""
        Write-Host "--- Building Docker images and starting services... (This may take a few minutes on the first run) ---" -ForegroundColor Yellow
        docker-compose up --build -d
        
        # Step 4: Provide clear, actionable information
        Write-Host ""
        Write-Host "--- ✅ Success! Services are running. ---" -ForegroundColor Green
        Write-Host ""
        Write-Host "   - Frontend Viewer is available at: http://localhost:5173"
        Write-Host "   - Backend API is available at:      http://localhost:8000"
        Write-Host "   - MinIO Storage Console at:       http://localhost:9090"
        Write-Host ""
        Write-Host "--- Tailing logs (Press Ctrl+C in this terminal to stop everything) ---" -ForegroundColor Cyan
        
        # Step 5: Attach to logs
        docker-compose logs -f
        ```
    *   **Rationale:** Providing a native PowerShell script demonstrates attention to detail and a commitment to a good developer experience on all major platforms. The logic, including error checking and graceful shutdown, is identical to the bash version.

---

#### **Phase 3: Documentation and Finalization**

**Goal:** To make the new scripts discoverable and easy to use by updating the project's primary documentation.

*   **Sub-Task 4.4.7: Update the `README.md` Quick Start Section**
    *   **Action:** Edit the root `README.md` file. Replace the existing Quick Start section with a new, clearer version that directs users to the correct script for their OS.
    *   **Content:**
        ```markdown
        ## 🚀 Quick Start: The 5-Minute Demo

        Get a working demo of OSSGameForge running on your machine in minutes. This will start the application in **Demo Mode**, which uses pre-made sample content for instant results.

        **Prerequisites:**
        *   Git
        *   Docker & Docker Compose

        ### Step 1: Clone the Repository
        ```bash
        git clone https://github.com/ClayKa/oss-game-forge.git
        cd oss-game-forge
        ```

        ### Step 2: Run the Demo Script for Your OS

        #### For Linux or macOS:
        Open your terminal and run:
        ```bash
        ./run_demo.sh
        ```

        #### For Windows (using PowerShell):
        Open PowerShell, navigate to the project directory, and run:
        ```powershell
        # You may need to change your execution policy first:
        # Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope Process
        .\run_demo.ps1
        ```

        ### Step 3: View the Application
        Once the script finishes, open your web browser and navigate to **`http://localhost:5173`**.

        To stop the application, go back to your terminal and press `Ctrl+C`.
        ```
    *   **Rationale:** This documentation is now foolproof. It explicitly tells users what they need and which command to run based on their operating system, removing all guesswork. The note about PowerShell's execution policy is a critical detail that will prevent a common source of frustration for Windows users.

*   **Sub-Task 4.4.8: Commit the Scripts and Documentation**
    *   **Action:** Commit `run_demo.sh`, `run_demo.ps1`, and the updated `README.md` to your feature branch and open a pull request.
    *   **Verification:** Ask a team member on a different OS to review the PR and, most importantly, to test the script for their platform to confirm it works as described.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Scripts Exist and are Executable:** Both `run_demo.sh` (with `+x` permissions) and `run_demo.ps1` are present in the root of the repository.
2.  **Scripts are Functional:** Each script successfully starts the Docker Compose stack in the correct demo mode and provides clear instructions to the user.
3.  **Documentation is Clear and Cross-Platform:** The `README.md` file provides simple, copy-pasteable instructions for users on both Unix-like systems and Windows.
4.  **A Non-Developer Can Run the Project:** The ultimate test is met: a user with no prior knowledge of the project's architecture can clone the repository, run a single command appropriate for their OS, and see the working application in their browser.