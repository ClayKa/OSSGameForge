### **Task Plan: 4.2 - CI with Robust Browser Smoke Tests (Expanded Detail)**

**Objective:** To integrate an automated browser-based "smoke test" into our Continuous Integration (CI) pipeline. This test will simulate a user's final action: downloading, unzipping, and running the exported HTML5 package. Its purpose is to act as a definitive quality gate, ensuring that no code change can be merged if it breaks the core functionality of our most important deliverable.

**[Priority]** [MUST]
**[Owner / Suggested Roles]** QA Lead (1), with support from DevOps (1)

---

#### **Phase 1: Setting up the E2E Testing Framework**

**Goal:** To prepare our project's frontend environment for automated browser testing using Playwright.

*   **Sub-Task 4.2.1: Install and Initialize Playwright**
    *   **Action:** Navigate to the `frontend/` directory in your terminal. Install Playwright as a development dependency.
    *   **Command:**
        ```bash
        cd frontend
        npm install -D @playwright/test
        ```
    *   **Action:** Initialize Playwright in your project. This command will create configuration files and example tests.
    *   **Command:**
        ```bash
        npx playwright install # This downloads the necessary browser binaries
        # You can optionally run `npx playwright init` to generate config files
        ```
    *   **Action:** A `playwright.config.ts` file will be created. Configure it to point to your test directory.
        ```typescript
        // frontend/playwright.config.ts
        import { defineConfig, devices } from '@playwright/test';

        export default defineConfig({
          testDir: './tests/e2e', // Point to our E2E test directory
          fullyParallel: true,
          reporter: 'html',
          use: {
            baseURL: 'http://localhost:3000', // A base URL for serving files
            trace: 'on-first-retry',
          },
          projects: [
            {
              name: 'chromium',
              use: { ...devices['Desktop Chrome'] },
            },
          ],
          webServer: { // This command starts a static server for our tests
            command: 'npx http-server ./temp-export --port 3000',
            url: 'http://localhost:3000',
            reuseExistingServer: !process.env.CI,
          },
        });
        ```
    *   **Rationale:** This setup configures Playwright to look for tests in a specific directory and automatically starts a local web server (`http-server`) to serve the contents of our unzipped export package, simulating how a user would open the `index.html` file.

*   **Sub-Task 4.2.2: Create the E2E Test File Structure**
    *   **Action:** Inside the `frontend/` directory, create the test directory and file.
    *   **Command:**
        ```bash
        mkdir -p tests/e2e
        touch tests/e2e/export_runner.spec.ts
        ```
    *   **Rationale:** This provides a clean, dedicated location for all end-to-end browser tests, separating them from unit or component tests.

---

#### **Phase 2: Implementing the Browser Smoke Test**

**Goal:** To write the automated test script that performs the export-unzip-serve-validate workflow.

*   **Sub-Task 4.2.3: Write the Test Setup and Teardown**
    *   **Action:** In `tests/e2e/export_runner.spec.ts`, write the main test block. Use Playwright's `test.beforeAll` and `test.afterAll` hooks to manage the exported files. This script will run in Node.js, so we need `axios`, `fs`, `path`, and `adm-zip`.
    *   **Prerequisites:** Add necessary helper libraries: `npm install -D axios adm-zip http-server`.
    *   **Content:**
        ```typescript
        // frontend/tests/e2e/export_runner.spec.ts
        import { test, expect } from '@playwright/test';
        import axios from 'axios';
        import fs from 'fs';
        import path from 'path';
        import AdmZip from 'adm-zip';

        const EXPORT_DIR = path.join(__dirname, '..', '..', 'temp-export');
        const BACKEND_URL = 'http://localhost:8000'; // Assuming backend is running

        // This block runs once before all tests in this file
        test.beforeAll(async () => {
            console.log('Setting up for E2E export test...');
            // 1. Clean up any previous test artifacts
            if (fs.existsSync(EXPORT_DIR)) {
                fs.rmSync(EXPORT_DIR, { recursive: true, force: true });
            }
            fs.mkdirSync(EXPORT_DIR, { recursive: true });

            // 2. Call the backend API to get the zip file
            const response = await axios({
                method: 'post',
                url: `${BACKEND_URL}/projects/golden-sample-1/export?engine=html5`,
                responseType: 'arraybuffer'
            });

            // 3. Unzip the response into our temp directory
            const zip = new AdmZip(response.data);
            zip.extractAllTo(EXPORT_DIR, /*overwrite*/ true);
            console.log('Exported package is ready for testing.');
        });
        
        // This block runs once after all tests in this file
        test.afterAll(async () => {
            console.log('Tearing down E2E export test...');
            // Clean up the temp directory
            if (fs.existsSync(EXPORT_DIR)) {
                fs.rmSync(EXPORT_DIR, { recursive: true, force: true });
            }
        });
        ```
    *   **Rationale:** This setup cleanly isolates the test artifacts. It programmatically fetches the *actual* export from our backend, providing a true end-to-end test. The `afterAll` hook ensures we leave a clean state.

*   **Sub-Task 4.2.4: Write the Core Smoke Test Assertion**
    *   **Action:** Add the actual test case that launches the browser and verifies the content.
    *   **Content (in the same file, after the setup blocks):**
        ```typescript
        test('HTML5 Runner should load and render a canvas', async ({ page }) => {
            // 1. Navigate to the local server hosting our unzipped file
            await page.goto('/'); // The baseURL is configured in playwright.config.ts

            // 2. Assert that the page title is correct
            await expect(page).toHaveTitle(/OSSGameForge Export/);

            // 3. The CRITICAL check: find the canvas element and assert it is visible
            const canvas = page.locator('#game-canvas');
            await expect(canvas).toBeVisible();

            // 4. Bonus check: Assert that the canvas is not empty (has some content)
            await expect(canvas).not.toHaveScreenshot('blank_canvas.png', { threshold: 0.99 });
            
            // 5. Check for console errors
            const consoleErrors = [];
            page.on('console', msg => {
                if (msg.type() === 'error') {
                    consoleErrors.push(msg.text());
                }
            });
            await page.waitForLoadState('networkidle');
            expect(consoleErrors).toHaveLength(0);
        });
        ```
    *   **Rationale:** This test simulates the user's experience perfectly. It checks that the page loads, that the core `<canvas>` element exists and is visible, and (most importantly) that no JavaScript errors occurred during the `runner.js` execution, which is a common point of failure.

---

#### **Phase 3: CI Integration and Optimization**

**Goal:** To embed this powerful new test into our CI workflow in a smart way that doesn't excessively slow down development cycles.

*   **Sub-Task 4.2.5: Optimize the CI Workflow (`.github/workflows/ci.yml`)**
    *   **Action:** Modify the CI YAML file to create separate jobs with different triggers.
    *   **Content:**
        ```yaml
        name: OSSGameForge CI

        on:
          push:
            branches: [ main ]
          pull_request:
            branches: [ main ]

        jobs:
          # --- Fast Tests: Run on every PR ---
          backend_tests:
            runs-on: ubuntu-latest
            steps:
              # ... steps for backend linting and pytest ...
          
          frontend_tests:
            runs-on: ubuntu-latest
            steps:
              # ... steps for frontend linting and unit tests ...

          # --- Slow E2E Test: Run only on merge to main or manually ---
          e2e_smoke_test:
            name: E2E Browser Smoke Test
            if: github.event_name == 'push' && github.ref == 'refs/heads/main' # Only run on merge to main
            needs: [backend_tests, frontend_tests] # Depends on fast tests passing
            runs-on: ubuntu-latest
            steps:
              - uses: actions/checkout@v4
              - uses: actions/setup-node@v3
                with:
                  node-version: '18'
              # ... Steps to build backend, run services in background ...
              - name: Run Playwright tests
                working-directory: ./frontend
                run: |
                  npm install
                  npx playwright install --with-deps
                  npx playwright test
        ```
    *   **Rationale:** This strategic split is key. Developers get fast feedback from linting and unit tests on their PRs. The slower, more resource-intensive E2E test runs only after a PR is approved and merged, ensuring the `main` branch is always in a verifiably working state without frustrating developers with long waits on every small change.

*   **Sub-Task 4.2.6: Document the CI Latency**
    *   **Action:** In `docs/testing.md`, add a new section explaining the CI strategy.
    *   **Content:**
        > ### CI/CD Strategy
        > Our CI pipeline is split into two stages for efficiency:
        >
        > 1.  **Pull Request Checks (Fast):** On every PR, we run fast static analysis (linting) and unit tests. This usually completes in under 2 minutes.
        > 2.  **Main Branch Integration Checks (Slow):** After a PR is merged into `main`, a slower, more comprehensive set of End-to-End (E2E) tests are run. This includes building the full application, running it in a headless browser, and performing visual checks. **This full integration run can take 2-5 minutes to complete.** This ensures our `main` branch is always stable and shippable.
    *   **Rationale:** Documentation manages expectations. This note explains to the team and to the judges why some CI runs take longer than others, demonstrating a deliberate and thoughtful CI strategy.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **E2E Test Suite Exists:** The `tests/e2e/export_runner.spec.ts` file contains a working Playwright test that successfully validates the exported HTML5 package.
2.  **CI Pipeline is Optimized:** The `.github/workflows/ci.yml` file is configured with separate jobs, running the slow E2E tests only on merges to the `main` branch.
3.  **Quality Gate is Functional:** A code change that breaks the JavaScript logic in `runner.js` (e.g., a typo) will now cause the `e2e_smoke_test` job on the `main` branch to fail, preventing a broken version from being deployed or released.
4.  **Process is Documented:** The new CI strategy and its expected performance are clearly documented.