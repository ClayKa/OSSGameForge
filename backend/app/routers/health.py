"""
Health check router for monitoring service status

Provides endpoints to verify application and dependency health.
"""
from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from ..config import settings
from ..database import check_db_connection, get_db

router = APIRouter()


@router.get("/", response_model=dict[str, Any])
async def check_health(db: Session = Depends(get_db)):
    """
    Health check endpoint for monitoring

    Returns the status of the application and its dependencies.
    Used by load balancers and monitoring systems.
    """
    health_status = {
        "status": "healthy",
        "version": settings.app_version,
        "environment": "development" if settings.debug else "production",
        "services": {}
    }

    # Check database connectivity
    try:
        # Execute a simple query to verify database connection
        db.execute(text("SELECT 1"))
        health_status["services"]["database"] = {
            "status": "ok",
            "type": "postgresql"
        }
    except Exception as e:
        health_status["status"] = "degraded"
        health_status["services"]["database"] = {
            "status": "error",
            "error": str(e)
        }

    # Check MinIO connectivity (if not in mock mode)
    if not settings.mock_mode:
        try:
            # In production, we would check MinIO connection here
            health_status["services"]["storage"] = {
                "status": "ok",
                "type": "minio"
            }
        except Exception as e:
            health_status["status"] = "degraded"
            health_status["services"]["storage"] = {
                "status": "error",
                "error": str(e)
            }
    else:
        health_status["services"]["storage"] = {
            "status": "mocked",
            "type": "minio"
        }

    # Check model service status
    health_status["services"]["inference"] = {
        "status": "ok" if settings.use_local_model else "fallback",
        "mode": "local_model" if settings.use_local_model else "golden_samples"
    }

    return health_status


@router.get("/ready", response_model=dict[str, bool])
async def check_readiness():
    """
    Readiness check endpoint

    Returns whether the service is ready to accept requests.
    Different from health check - this indicates if the service
    is fully initialized and ready.
    """
    # Check if database is accessible
    db_ready = check_db_connection()

    # In production, check other initialization requirements
    services_ready = True  # Placeholder for additional checks

    is_ready = db_ready and services_ready

    if not is_ready:
        raise HTTPException(status_code=503, detail="Service not ready")

    return {"ready": is_ready}


@router.get("/live", response_model=dict[str, bool])
async def check_liveness():
    """
    Liveness check endpoint

    Simple endpoint to verify the service is alive.
    Used by Kubernetes or other orchestrators for liveness probes.
    """
    return {"alive": True}
