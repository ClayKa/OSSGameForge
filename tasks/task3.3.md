### **Task Plan: 3.3 - Demo Video Scripting Tied to Golden Samples (Expanded Detail)**

**Objective:** To proactively design and document the narrative and visual flow of our final 3-minute demonstration video. By creating a detailed script and shot list tied to a specific, predictable "Golden Sample," we eliminate the risks associated with live demos and last-minute creative decisions. This task transforms video production from a potential bottleneck into a simple execution of a well-rehearsed plan.

**[Priority]** [MUST - Risk Management]
**[Owner / Suggested Roles]** All Team Members (for the initial brainstorm), designated Project Manager or UX Lead (as the "Scribe" and owner of the final document).

---

#### **Phase 1: Narrative and Storyboard Development**

**Goal:** To define the core message and story we want to tell the judges in under 3 minutes.

*   **Sub-Task 3.3.1: Host a Demo Brainstorming Session**
    *   **Action:** Schedule a 45-minute meeting with the entire team.
    *   **Agenda:**
        1.  (5 min) Re-state the objective: What are the 1-3 key takeaways we want the judges to have after watching our video? (e.g., "It's a fast, easy way to create games," "It's a resilient and well-engineered tool.")
        2.  (20 min) Brainstorm the "story." What is the user's journey? It should follow our core MVP loop: The Problem -> Our Solution (Upload) -> The Magic (Generate) -> The Result (View) -> The Proof (Export & Run).
        3.  (15 min) Agree on the specific "Golden Sample" to use for the entire demonstration. The `sample_simple_geometry.json` is the safest and clearest choice, as it's easy to understand visually.
    *   **Rationale:** This collaborative session ensures team buy-in and captures the best ideas. Agreeing on the core message and sample provides the scribe with a clear mandate.

*   **Sub-Task 3.3.2: Create the Master Script Document**
    *   **Action:** Create a new file at `docs/demo_script.md`.
    *   **Action:** At the very top of this file, add the explicit "Binding Declaration." This is a non-negotiable directive for the final recording.
        ```markdown
        # OSSGameForge - Final Demo Video Script (v1)

        **IMPORTANT NOTE FOR THE TEAM:** This entire demonstration video will be recorded using the `sample_simple_geometry.json` golden sample as the output of the generation step. The objective is to show the full, stable end-to-end loop with a predictable and reproducible result. **Do not use the live model (`USE_LOCAL_MODEL=true`) for any part of the final video recording.**
        ```
    *   **Rationale:** This declaration acts as a "guard rail," preventing any deviation during the stressful final week. It ensures the recorded demo is as stable and reliable as our CI tests.

---

#### **Phase 2: Detailed Script and Shot List Creation**

**Goal:** To write the exact script, second by second, mapping narration to specific on-screen actions.

*   **Sub-Task 3.3.3: Draft the Timed Narration Script**
    *   **Action:** In `docs/demo_script.md`, create a table or formatted list to break down the video into timed segments. Write the exact words that will be spoken as narration or shown as on-screen text.
    *   **Example Content:**
        | Time       | Narration / On-Screen Text                                                                  |
        |------------|---------------------------------------------------------------------------------------------|
        | 0:00-0:05  | **[TITLE CARD]** OSSGameForge: AI-Powered Game Creation. (Upbeat, simple music starts)        |
        | 0:05-0:15  | "Bringing game ideas to life is complex. OSSGameForge makes it simple, fast, and reliable."   |
        | 0:15-0:30  | "Let's create a level. First, we upload our assets, confirming we have the rights to use them." |
        | 0:30-0:45  | "Next, we give the AI a simple prompt and click 'Generate'."                                |
        | 0:45-1:00  | "Instantly, our level is generated and visualized in the editor."                           |
        | ...        | ...                                                                                         |

*   **Sub-Task 3.3.4: Create the Corresponding Shot List**
    *   **Action:** For each line of narration, specify the exact visual that should be on screen. Be extremely specific.
    *   **Example Content (to be added to the same table):**
        | Time       | Narration / On-Screen Text                                       | **On-Screen Action (Shot List)**                                                                              |
        |------------|------------------------------------------------------------------|---------------------------------------------------------------------------------------------------------------|
        | 0:15-0:30  | "Let's create a level. First, we upload our assets..."           | Mouse cursor moves to the "Upload Asset" button. File dialog opens. A `player.png` is selected. The "I consent" checkbox is ticked. The "Upload" button is clicked. |
        | 0:30-0:45  | "Next, we give the AI a simple prompt and click 'Generate'."       | Cursor types "A simple platformer level" into a text box. The "Generate" button is clicked. A loading spinner appears for 1-2 seconds. |
        | 0:45-1:00  | "Instantly, our level is generated and visualized in the editor."| The spinner disappears. The canvas instantly populates with the platforms and player from the `sample_simple_geometry.json`. The mouse pans across the canvas to show the full scene. |
        | ...        | ...                                                              | ...                                                                                                           |

    *   **Rationale:** This level of detail removes all ambiguity. The person recording the video in Week 6 doesn't have to think or improvise; they simply follow the shot list like a recipe.

---

#### **Phase 3: Review and Finalization**

**Goal:** To get final approval on the script from the team, ensuring it accurately reflects the project's strengths.

*   **Sub-Task 3.3.5: Conduct a Script Review**
    *   **Action:** Create a Pull Request for the `docs/demo_script.md` file.
    *   **Action:** Assign all team members as reviewers. Ask them to read through the script and shot list and provide feedback. Key questions for review:
        *   Is the message clear?
        *   Is it under 3 minutes? (Read the narration aloud and time it).
        *   Does it highlight our key strengths (resilience, speed via fallback, clean UI, verifiable export)?
        *   Is every action specified in the shot list feasible with our current MVP?
    *   **Action:** Incorporate feedback and merge the pull request.
    *   **Rationale:** Treating the script as a piece of code that requires a review ensures its quality and alignment with the team's vision.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **A Complete Script Exists:** The file `docs/demo_script.md` is committed to the main branch of the repository.
2.  **The Script is Reproducible:** The script explicitly states that it will be demonstrated using a specific, named golden sample file, ensuring the final recorded demo is predictable.
3.  **The Script is Actionable:** The script contains a detailed, timed shot list that maps every moment of narration to a specific on-screen action, serving as a complete set of instructions for the person who will perform the screen recording in the final weeks.
4.  **Team Alignment is Achieved:** The entire team has reviewed and approved the narrative and flow of the final demo, ensuring a unified vision for the project's presentation.