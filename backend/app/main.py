"""
OSSGameForge Backend API
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Import routers (will be added as we develop)
# from .routers import health, assets, generation, export

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    # Startup
    logger.info("Starting OSSGameForge Backend...")
    logger.info(f"Mock Mode: {os.getenv('MOCK_MODE', 'false')}")
    logger.info(f"Local Model: {os.getenv('USE_LOCAL_MODEL', 'false')}")
    yield
    # Shutdown
    logger.info("Shutting down OSSGameForge Backend...")

# Create FastAPI app
app = FastAPI(
    title="OSSGameForge API",
    description="AI-powered game creation suite backend",
    version="0.1.0",
    lifespan=lifespan
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React dev servers
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    """
    Health check endpoint for monitoring
    """
    return {
        "status": "healthy",
        "service": "ossgameforge-backend",
        "version": "0.1.0",
        "mock_mode": os.getenv("MOCK_MODE", "false") == "true",
        "use_local_model": os.getenv("USE_LOCAL_MODEL", "false") == "true"
    }

# Root endpoint
@app.get("/")
async def root():
    """
    Root endpoint with API information
    """
    return {
        "message": "Welcome to OSSGameForge API",
        "documentation": "/docs",
        "health": "/health"
    }

# Register routers (uncomment as they are implemented)
# app.include_router(health.router, prefix="/api/health", tags=["Health"])
# app.include_router(assets.router, prefix="/api/assets", tags=["Assets"])
# app.include_router(generation.router, prefix="/api/generation", tags=["Generation"])
# app.include_router(export.router, prefix="/api/export", tags=["Export"])