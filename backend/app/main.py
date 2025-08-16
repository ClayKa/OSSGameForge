"""
OSSGameForge Backend API
Main FastAPI application entry point
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import logging

from .config import settings
from .database import init_db
from .routers import projects, assets, generation, export, health

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Manage application lifecycle
    """
    # Startup
    logger.info("Starting OSSGameForge Backend...")
    logger.info(f"Mock Mode: {settings.mock_mode}")
    logger.info(f"Local Model: {settings.use_local_model}")
    
    # Initialize database tables if not in mock mode
    if not settings.mock_mode:
        try:
            init_db()
            logger.info("Database initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database: {e}")
            # Continue anyway in development, but in production this should fail
            if not settings.debug:
                raise
    
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

# Include health router for comprehensive health checks
app.include_router(health.router, prefix="/health", tags=["Health"])

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

# Register routers
app.include_router(projects.router, prefix="/api/projects", tags=["Projects"])
app.include_router(assets.router, prefix="/api", tags=["Assets"])
app.include_router(generation.router, prefix="/api/generation", tags=["Generation"])
app.include_router(export.router, prefix="/api", tags=["Export"])