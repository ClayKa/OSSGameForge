# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

OSSGameForge is an AI-powered game creation suite for a hackathon competition. It enables users to upload assets and generate game scenes using AI, with a focus on a minimal viable product approach.

## Development Overview

See @ROADMAP.md for current status and coming tasks.
Remember to write tests for all tasks.
Every time finish a Week or a Task, add a ✅ after them, such as ### "**Task 1.1 (Corrected): Project Init, Version Control & CI** ✅".

## Project Structure

```
oss-game-forge/
├── backend/          # FastAPI server-side code
│   └── app/
│       ├── services/    # Business logic (context_builder, inference_client, postprocessor)
│       ├── routers/     # API endpoints
│       ├── runners/     # HTML5 runner templates
│       └── golden_samples/  # Test samples for validation
├── frontend/         # React client-side code
│   └── src/
├── devops/          # Docker configuration and mocks
│   └── mocks/
├── docs/            # Documentation
│   ├── api_contracts/   # API specifications
│   ├── testing.md      # Testing documentation
│   └── demo_script.md  # Demo video script
├── tests/           # Automated tests
│   ├── backend/
│   └── e2e/            # End-to-end tests with Playwright
└── tasks/           # Detailed task plans for implementation

```

## Key Commands

### Initial Setup

```bash
# Clone repository
git clone https://github.com/ClayKa/oss-game-forge.git
cd oss-game-forge

# Start services with Docker
docker-compose up --build -d

# For demo mode (fallback without GPU)
USE_LOCAL_MODEL=false docker-compose up
```

### Development Commands

```bash
# Backend linting
ruff check backend

# Run backend tests  
pytest tests/backend

# Run full CI suite locally
pytest && ruff check backend

# Install frontend dependencies
cd frontend && npm install

# Run frontend development server
npm run dev

# Run E2E tests with Playwright
npm run test:e2e
```

### Git Workflow

```bash
# Create feature branch (main is protected)
git checkout -b feature/your-feature-name

# After changes, push and create PR
git add .
git commit -m "feat: your feature description"
git push -u origin feature/your-feature-name
```

### Cross-Platform Demo Scripts

```bash
# Linux/macOS
./run_demo.sh

# Windows PowerShell
./run_demo.ps1
```

## Core API Endpoints

- `POST /projects/{project_id}/assets` - Upload assets with consent validation
- `POST /generate` - Generate game scene from prompt
- `POST /export?engine=html5` - Export scene as playable HTML5 package
- `GET /assets/{asset_id}` - Retrieve asset metadata

## Architecture & Key Components

### Backend Services (Modular Design)

1. **context_builder.py** - Constructs prompts for AI generation
2. **inference_client.py** - Handles model inference with fallback mechanism
3. **postprocessor.py** - Processes AI output into scene JSON
4. **asset_service.py** - Manages asset upload, EXIF stripping, metadata extraction

### Database Models

- **Asset**: Tracks uploaded files with consent, EXIF stripping status, and metadata
- **GenerationLog**: Audit log for all generation requests with performance metrics

### Testing Strategy

- **Golden Samples**: 3 predefined test cases in `backend/app/golden_samples/`
  - Sample 1: Simple geometry testing
  - Sample 2: Asset-intensive scenarios  
  - Sample 3: Complex JSON structures
- **CI Pipeline**: Automated checks on all PRs (linting + tests)
- **E2E Tests**: Playwright browser tests validating exported HTML5 runners

## Environment Variables

```bash
# Core Settings
MOCK_MODE=true/false         # Enable mock API responses for frontend development
USE_LOCAL_MODEL=true/false   # Toggle between local model and fallback mode

# Storage
MINIO_ENDPOINT=localhost:9000
MINIO_ACCESS_KEY=minioadmin
MINIO_SECRET_KEY=minioadmin

# Database
DATABASE_URL=postgresql://user:password@postgres:5432/ossgameforge
```

## Performance Expectations

- **Fallback Mode** (USE_LOCAL_MODEL=false): Instant responses using predefined samples
- **Local Model Mode**: 15-45 seconds latency, requires GPU with >=16GB VRAM
- **CI Pipeline**: 2-5 minutes for full test suite

## Critical Implementation Notes

1. **Branch Protection**: Direct pushes to `main` are blocked; all changes require PR with passing CI
2. **User Consent**: All asset uploads require explicit `user_consent: true` parameter
3. **EXIF Stripping**: Automatic for all uploaded images before storage
4. **Async Processing**: Uses FastAPI BackgroundTasks for non-blocking operations
5. **Error Handling**: Graceful fallbacks for model failures and corrupt files

## Current Implementation Status

Based on the task files, the project follows a 6-week development plan:
- Week 1: Foundation, CI/CD, and mock APIs ✅
- Week 2: Core generation pipeline with resilience
- Week 3: Frontend viewer and editor capabilities
- Week 4: HTML5 export and browser testing
- Weeks 5-6: Polish, testing, and demo preparation

The codebase prioritizes the "MUST-HAVE" features for MVP while deferring complex features like Unity export and LoRA fine-tuning.

## Development Progress

### Completed Tasks
- **Task 1.1**: Project initialization, version control, and CI/CD setup ✅
  - Created comprehensive directory structure
  - Configured Docker Compose with PostgreSQL and MinIO
  - Implemented CI/CD pipeline with quality gates
  - Added pre-commit hooks and security scanning
  - Created demo scripts for easy setup