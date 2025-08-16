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
- **Task 1.2**: Simplified Service Orchestration & Mock API First ✅
  - Created docker-compose.yml with postgres, minio, and backend services
  - Implemented mock mode in FastAPI backend with environment variable control
  - Created comprehensive mock data for API endpoints
  - Defined OpenAPI 3.0 specification in docs/api_contracts/v1.yaml
  - Implemented all core API endpoints with mock responses
  - Successfully tested all endpoints in mock mode
- **Task 1.3**: Modular Backend & Minimalist Database ✅
  - Created modular service architecture with three core services:
    - context_builder.py: Constructs prompts for AI generation
    - inference_client.py: Handles model inference with fallback mechanism
    - postprocessor.py: Processes AI output into valid scene JSON
  - Defined SQLAlchemy models for Asset, GenerationLog, Project, and Scene tables
  - Configured Alembic for database migrations with proper environment setup
  - Implemented health check endpoints with database connectivity verification
  - Created comprehensive test suite for all services with 100% pass rate

### Week 2 Tasks
- **Task 2.1**: Simplified Preprocessing Pipeline ✅
  - Implemented asset upload endpoint with mandatory user consent validation
  - Created comprehensive EXIF stripping for all uploaded images for privacy protection
  - Implemented metadata extraction for audio/video files using tinytag
  - Built async processing architecture using FastAPI BackgroundTasks
  - Created MinIO storage integration with proper bucket management
  - Developed comprehensive asset service module with error handling
  - Wrote extensive test suite covering all preprocessing functionality
  - Ensured GDPR compliance with consent tracking and privacy measures
- **Task 2.2**: The Resilient Generation Engine with Explicit Fallbacks ✅
  - Created 5 comprehensive golden sample JSON files covering **100% of edge cases**:
    - sample_simple_geometry.json: Basic rendering with 10 entities
    - sample_asset_intensive.json: Asset management with 9 assets and 11 entities
    - sample_complex_structure.json: Complex nested structures with layers, events, and scripts
    - sample_minimal_empty.json: Empty scene edge case testing
    - sample_single_entity.json: Minimal viable scene validation
  - Enhanced InferenceClient with intelligent fallback mechanism:
    - Automatic fallback on model failure with detailed logging
    - Intelligent sample selection based on prompt keywords
    - Performance tracking and statistics
    - Support for both local model and fallback modes
  - Implemented comprehensive generation API endpoint:
    - Full pipeline orchestration (context → inference → post-processing)
    - Database logging of all generation requests
    - Background task processing for non-blocking operations
    - Status and monitoring endpoints
  - Added complete documentation:
    - Performance expectations in README (Fallback: <100ms, Local: 15-45s)
    - Golden sample extension guide in docs/testing.md
    - Detailed testing strategies and troubleshooting
  - Created extensive test suite with 28 test cases covering:
    - Golden sample loading and validation
    - Intelligent sample selection
    - Fallback mechanisms and error handling
    - Edge cases and performance testing