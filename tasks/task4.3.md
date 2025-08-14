### **Task Plan: 4.3 - Visual Consistency Check with Tolerance (Expanded Detail)**

**Objective:** To implement an automated visual regression test that programmatically compares screenshots of the in-app "Viewer" and the final exported "HTML5 Runner." This test will be configured with specific tolerance and retry mechanisms to be robust against minor, insignificant rendering differences, ensuring it only fails when a genuine visual inconsistency is introduced.

**[Priority]** [SHOULD]
**[Owner / Suggested Roles]** QA Lead (1), with support from Frontend Engineer (1)

---

#### **Phase 1: Setting up the Visual Testing Framework**

**Goal:** To prepare our E2E test environment with the necessary tools and configurations for performing image-based comparisons.

*   **Sub-Task 4.3.1: Install Image Comparison Dependencies**
    *   **Action:** Navigate to the `frontend/` directory. Install the libraries needed for image processing and comparison.
    *   **Command:**
        ```bash
        npm install -D pixelmatch pngjs
        ```
    *   **Rationale:**
        *   `pixelmatch`: A fast and simple pixel-level image comparison library, which will be the core of our test.
        *   `pngjs`: A dependency for `pixelmatch` that allows it to decode and encode PNG image data in a Node.js environment.

*   **Sub-Task 4.3.2: Configure Playwright for Visual Testing**
    *   **Action:** Open the `frontend/playwright.config.ts` file. We will add configurations specifically for visual tests, including retries and snapshot paths.
    *   **Content:**
        ```typescript
        // frontend/playwright.config.ts
        import { defineConfig, devices } from '@playwright/test';

        export default defineConfig({
          // ... other configurations ...
          testDir: './tests/e2e',
          snapshotDir: './tests/e2e/snapshots', // Designate a folder for snapshots
          
          expect: {
            // Default timeout for expect() calls, including toHaveScreenshot
            timeout: 5000,
            // Configure snapshot assertion options
            toHaveScreenshot: {
              maxDiffPixels: 10, // Allow a very small number of pixels to be different
            },
          },

          // Enable retries specifically for CI environments to handle flakes
          retries: process.env.CI ? 1 : 0,
          
          projects: [ /* ... */ ],
          webServer: { /* ... */ },
        });
        ```
    *   **Rationale:** Configuring `snapshotDir` keeps our test artifacts organized. Setting a global `maxDiffPixels` and enabling `retries` in the main configuration file makes our test suite more resilient against "flakiness" caused by tiny, non-deterministic rendering differences (like font anti-aliasing) in different CI environments.

---

#### **Phase 2: Implementing the Visual Comparison Test**

**Goal:** To write the E2E test script that captures screenshots from both the live viewer and the exported runner and then compares them.

*   **Sub-Task 4.3.3: Create a New E2E Test File**
    *   **Action:** In `frontend/tests/e2e/`, create a new file named `visual_consistency.spec.ts`.
    *   **Rationale:** Separating this test from the basic "smoke test" allows us to run them independently and apply different configurations (like more retries) if needed.

*   **Sub-Task 4.3.4: Write the Viewer Snapshot Test**
    *   **Action:** Write the first test case in the new file. This test will navigate to our live application's viewer, load a specific golden sample, and take a "golden" snapshot.
    *   **Content:**
        ```typescript
        // frontend/tests/e2e/visual_consistency.spec.ts
        import { test, expect } from '@playwright/test';

        test('Viewer canvas should match the golden snapshot', async ({ page }) => {
            // 1. Navigate to the editor page of the application
            // This assumes the frontend app is running and can load a specific scene
            await page.goto('/editor/golden-sample-simple-geometry');

            // 2. Find the canvas element
            const canvas = page.locator('#editor-canvas-konva'); // Assuming your viewer canvas has a specific ID

            // 3. Wait for any animations or rendering to settle
            await page.waitForLoadState('networkidle');

            // 4. Take the snapshot and compare it to a stored version
            // The first time this runs, it will create 'viewer-golden.png' in the snapshot directory.
            // Subsequent runs will compare against this file.
            await expect(canvas).toHaveScreenshot('viewer-golden.png', {
                threshold: 0.1 // Per-snapshot threshold for color difference tolerance
            });
        });
        ```
    *   **Rationale:** Playwright's `toHaveScreenshot` is a powerful assertion. It automates the process of saving a baseline image and comparing against it on future runs. The `threshold` option gives us fine-grained control over color sensitivity, making the test robust against subtle rendering engine differences.

*   **Sub-Task 4.3.5: Write the Runner Comparison Test**
    *   **Action:** Write the second, more complex test case. This test will perform the export, launch the runner, and compare its canvas against the *same golden snapshot* taken in the previous test.
    *   **Content (in the same file):**
        ```typescript
        // ... imports from the smoke test (axios, fs, AdmZip) ...

        test('Exported Runner canvas should match the golden snapshot', async ({ page }) => {
            // SETUP: Perform the export and serve the runner (same logic as smoke test)
            // ... (Copy the beforeAll logic or refactor it into a helper function) ...
            // For simplicity, we assume this is done and the server is running.

            // 1. Navigate to the locally served runner
            await page.goto('/'); // Base URL points to our temp server

            // 2. Find the runner's canvas element
            const canvas = page.locator('#game-canvas');

            // 3. Wait for the runner.js to load and render
            await page.waitForLoadState('networkidle');

            // 4. CRITICAL CHECK: Compare the runner's canvas to the SAME snapshot
            // This test will FAIL if the runner's rendering is different from the viewer's.
            await expect(canvas).toHaveScreenshot('viewer-golden.png', {
                threshold: 0.1
            });
        });
        ```
    *   **Rationale:** This is the core of the visual consistency check. By comparing two different implementations (the React/Konva viewer vs. the vanilla JS runner) against a single "source of truth" snapshot, we are directly testing if "What You See" is *truly* "What You Get."

---

#### **Phase 3: CI Integration and Documentation**

**Goal:** To integrate this slower, more intensive test into our CI workflow intelligently and to document its behavior.

*   **Sub-Task 4.3.6: Update the CI Workflow**
    *   **Action:** Modify `.github/workflows/ci.yml` to include a dedicated job for this test.
    *   **Content:**
        ```yaml
        # In .github/workflows/ci.yml
        # ...
          visual_consistency_test:
            name: E2E Visual Consistency Test
            # Run only on merge to main, as it's slow and resource-intensive
            if: github.event_name == 'push' && github.ref == 'refs/heads/main'
            needs: e2e_smoke_test # Should only run if the basic smoke test passes
            runs-on: ubuntu-latest
            steps:
              # ... checkout, setup node, run services ...
              - name: Run Playwright Visual Tests
                working-directory: ./frontend
                run: npx playwright test visual_consistency.spec.ts
              
              # Optional: Upload test results and snapshots as artifacts
              - uses: actions/upload-artifact@v3
                if: failure()
                with:
                  name: playwright-report
                  path: playwright-report/
        ```
    *   **Rationale:** We explicitly run this test only on merges to `main`. This prevents it from slowing down the development cycle on pull requests but guarantees our main branch is always visually consistent. Uploading the report on failure is crucial for debugging, as it will contain the "actual," "expected," and "diff" images.

*   **Sub-Task 4.3.7: Document the Visual Testing Process**
    *   **Action:** In `docs/testing.md`, add a new section.
    *   **Content:**
        > ### Visual Regression Testing
        >
        > To ensure consistency between our in-app viewer and the final exported HTML5 runner, we perform automated visual regression testing using Playwright and Pixelmatch.
        >
        > **How it Works:**
        > 1. A "golden" screenshot is taken of a specific scene rendered in the main application viewer. This snapshot is stored in the repository at `frontend/tests/e2e/snapshots/`.
        > 2. The test then exports the same scene and runs it in a headless browser.
        > 3. A second screenshot is taken of the exported runner's canvas.
        > 4. The two images are compared pixel-by-pixel.
        >
        > **Tolerance & Retries:**
        > The test is configured with a `threshold` of 0.1 to ignore minor anti-aliasing differences between rendering environments. In CI, failed tests are automatically retried once to mitigate temporary flakiness.
        >
        > **Updating Snapshots:**
        > If a visual change is intentional, a developer must run `npx playwright test --update-snapshots` locally and commit the new golden snapshot along with their code changes.

*   **Rationale:** This documentation is essential for team collaboration. It explains why a test might fail, how to debug it (by looking at the artifacts), and the official process for updating the baseline snapshots when intended changes are made.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Test Suite Exists:** The file `tests/e2e/visual_consistency.spec.ts` is implemented.
2.  **Robust Configuration is in Place:** The `playwright.config.ts` file correctly configures snapshot directories, tolerance thresholds, and retries for CI.
3.  **CI Job is Integrated:** The CI workflow has a separate, conditional job for visual testing that uploads failure artifacts.
4.  **Consistency is Enforced:** A code change that causes the exported runner to render even slightly differently from the main viewer will result in a failed CI check on the `main` branch, preventing the inconsistency from being deployed.