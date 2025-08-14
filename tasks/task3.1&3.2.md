### **Task Plan: 3.1 & 3.2 - Viewer and Minimal Editing (Expanded Detail)**

**Objective:** To develop the primary user interface for our application: an interactive canvas that can accurately visualize the AI-generated `scene.json` data. The core goal is to create a high-fidelity "Viewer." The secondary, "stretch" goal is to add minimal interactivity through object selection and drag-and-drop.

**[Priority]** [MUST] for Viewing & Selection; [SHOULD] for Editing (Drag & Drop)
**[Owner / Suggested Roles]** Frontend Lead (1), Frontend Engineer (1)

---

#### **Phase 1: Scaffolding the Frontend for Visualization**

**Goal:** To set up the necessary components, state management stores, and data flow to get scene data from our API to a state where it's ready to be rendered.

*   **Sub-Task 3.1.1: Install and Configure Frontend Dependencies**
    *   **Step 1:** Navigate to the `frontend/` directory in your terminal.
    *   **Step 2:** Install the specific libraries required for this task.
        ```bash
        npm install zustand konva react-konva
        ```
    *   **Rationale:**
        *   `zustand`: A lightweight, simple state management library perfect for sharing state like the scene data and selected object ID across components.
        *   `konva` & `react-konva`: A powerful 2D canvas library and its React wrapper, ideal for our rendering needs.

*   **Sub-Task 3.1.2: Define the State Management Store**
    *   **Step 1:** In `frontend/src/`, create a new directory `stores`.
    *   **Step 2:** Inside, create `sceneStore.ts`. This store will be the single source of truth for all data related to the scene being viewed.
    *   **Step 3:** Define the store's state and actions.
        ```typescript
        // frontend/src/stores/sceneStore.ts
        import create from 'zustand';

        // Define the shape of our data (can be based on Pydantic models)
        interface SceneEntity {
          id: string;
          type: string;
          x: number;
          y: number;
          width?: number;
          height?: number;
          // ... other properties
        }
        
        interface SceneState {
          entities: SceneEntity[];
          selectedEntityId: string | null;
          fetchScene: (sceneId: string) => Promise<void>;
          setSelectedEntityId: (id: string | null) => void;
          updateEntityPosition: (id: string, newPosition: { x: number; y: number }) => void;
        }

        export const useSceneStore = create<SceneState>((set) => ({
          entities: [], // Start with an empty scene
          selectedEntityId: null,

          // Action to fetch data from the backend
          fetchScene: async (sceneId) => {
            // const response = await axios.get(`/api/scenes/${sceneId}`); // Or from /generate
            // set({ entities: response.data.entities });
          },

          // Action to update the selected entity
          setSelectedEntityId: (id) => set({ selectedEntityId: id }),

          // Action to update an entity's position locally
          updateEntityPosition: (id, newPosition) => set((state) => ({
            entities: state.entities.map(entity => 
              entity.id === id ? { ...entity, ...newPosition } : entity
            ),
          })),
        }));
        ```
    *   **Rationale:** This centralized store decouples our UI components from the data-fetching logic. Any component can subscribe to this store and will automatically re-render when the data changes, which is perfect for an interactive editor.

---

#### **Phase 2: Implementing the Read-Only Viewer**

**Goal:** To build the core functionality of rendering a static scene from the state store onto the canvas. This is the **MUST-HAVE** part of the task.

*   **Sub-Task 3.1.3: Create the Main Canvas Component**
    *   **Step 1:** In `frontend/src/components/`, create a new directory `editor`.
    *   **Step 2:** Inside, create `EditorCanvas.tsx`. This component will contain the main Konva `Stage`.
        ```typescript
        // frontend/src/components/editor/EditorCanvas.tsx
        import React, { useEffect } from 'react';
        import { Stage, Layer } from 'react-konva';
        import { useSceneStore } from '../../stores/sceneStore';
        // ... We will create SceneEntityComponent next

        export const EditorCanvas = () => {
          const { entities, fetchScene } = useSceneStore();
          
          useEffect(() => {
            // For now, let's load a mock scene or a golden sample
            // fetchScene("some-scene-id"); 
          }, [fetchScene]);

          return (
            <Stage width={window.innerWidth} height={window.innerHeight}>
              <Layer>
                {/* We will map entities to components here */}
              </Layer>
            </Stage>
          );
        };
        ```
    *   **Rationale:** This sets up the main container for our visualization. All other rendered objects will live inside this `Stage`.

*   **Sub-Task 3.1.4: Create a Generic Entity Renderer Component**
    *   **Step 1:** Inside `frontend/src/components/editor/`, create `SceneEntityComponent.tsx`. This component will be responsible for rendering a single entity from our scene data.
    *   **Step 2:** The component will take an `entity` object as a prop and use a `switch` statement or conditional logic to render the correct Konva shape based on the `entity.type`.
        ```typescript
        // frontend/src/components/editor/SceneEntityComponent.tsx
        import React from 'react';
        import { Rect, Image as KonvaImage, Text } from 'react-konva';
        // ... interface SceneEntity ...

        interface Props {
          entity: SceneEntity;
        }

        export const SceneEntityComponent: React.FC<Props> = ({ entity }) => {
          switch (entity.type) {
            case 'platform':
              return <Rect x={entity.x} y={entity.y} width={entity.width} height={entity.height} fill="grey" />;
            case 'player':
              return <Rect x={entity.x} y={entity.y} width={30} height={50} fill="blue" />;
            // Add cases for 'image', 'text', etc. later
            default:
              return null;
          }
        };
        ```
    *   **Rationale:** This modular approach keeps the main `EditorCanvas` clean. It makes it easy to add support for new entity types in the future by simply adding a new `case` to the `switch` statement.

*   **Sub-Task 3.1.5: Render the Full Scene**
    *   **Step 1:** In `EditorCanvas.tsx`, import the `SceneEntityComponent`.
    *   **Step 2:** Inside the `<Layer>`, use the `.map()` function on the `entities` array from the Zustand store to render a `SceneEntityComponent` for each entity. Pass the `entity` object and a unique `key`.
        ```typescript
        // Inside EditorCanvas.tsx's return statement
        <Layer>
          {entities.map(entity => (
            <SceneEntityComponent key={entity.id} entity={entity} />
          ))}
        </Layer>
        ```
    *   **Verification:** At this point, if you populate the Zustand store with mock data (e.g., from one of your golden samples), the shapes should appear on the canvas when the application loads.

---

#### **Phase 3: Adding Minimal Interactivity**

**Goal:** To enhance the viewer with selection and drag-and-drop capabilities. This is the **SHOULD-HAVE** part of the task.

*   **Sub-Task 3.2.1: Implement Object Selection and Highlighting**
    *   **Step 1:** Modify `SceneEntityComponent.tsx` to handle clicks and to visually change based on selection state.
    *   **Step 2:** Import the `useSceneStore` hook.
    *   **Step 3:** Get the `selectedEntityId` and `setSelectedEntityId` function from the store.
    *   **Step 4:** Add an `onClick` handler to the rendered Konva shape that calls `setSelectedEntityId(entity.id)`.
    *   **Step 5:** Add logic to change the appearance (e.g., `stroke`, `strokeWidth`) if the component's `entity.id` matches the `selectedEntityId` from the store.
        ```typescript
        // Inside SceneEntityComponent.tsx
        const { selectedEntityId, setSelectedEntityId } = useSceneStore();
        const isSelected = selectedEntityId === entity.id;

        // ... inside the return ...
        <Rect
          // ... other props
          onClick={() => setSelectedEntityId(entity.id)}
          stroke={isSelected ? 'red' : 'black'}
          strokeWidth={isSelected ? 2 : 0}
        />
        ```
    *   **Rationale:** This creates a direct feedback loop for the user. Clicking an object updates the global state, and the component re-renders itself with a new visual style based on that global state.

*   **Sub-Task 3.2.2: Implement Drag-and-Drop Functionality**
    *   **Step 1:** In `SceneEntityComponent.tsx`, get the `updateEntityPosition` action from the `useSceneStore`.
    *   **Step 2:** Add the `draggable` prop to the returned Konva shape.
        ```typescript
        // Inside SceneEntityComponent.tsx
        const { updateEntityPosition } = useSceneStore();

        // ... inside the return ...
        <Rect
          // ... other props
          draggable={true}
          onDragEnd={(e) => {
            updateEntityPosition(entity.id, { x: e.target.x(), y: e.target.y() });
          }}
        />
        ```
    *   **Rationale:** This is the final step for minimal editing. The `onDragEnd` event provides the new coordinates, and we call our pre-defined state management action to update the data. Because all components subscribe to the same store, any other part of the UI (like an Inspector panel) would automatically show the new coordinates. This is a "local-first" update, meaning it's fast and responsive, without waiting for a backend confirmation.

---

#### **Acceptance Criteria / Final State Verification**

Upon completion of this task plan:

1.  **Rendering is Correct:** Any valid `scene.json` (specifically, your golden samples) loaded into the Zustand store is rendered accurately on the canvas, with all specified entities appearing in their correct initial positions.
2.  **Selection Works:** Clicking on any entity on the canvas causes it to be visually highlighted (e.g., with a red border), and clicking on another entity or the background deselects it.
3.  **Drag and Drop is Functional:** Users can click and drag any entity to a new position on the canvas. When the mouse is released, the entity remains in the new position. This position change is reflected in the application's internal state (verifiable with React DevTools inspecting the Zustand store).
4.  **Scope is Contained:** The implementation has successfully created a functional viewer with basic interactivity, without building a complex property editor or timeline, thus meeting the MVP/SHOULD goals on schedule.