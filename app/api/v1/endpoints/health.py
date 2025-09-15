"""
Health check endpoints
"""
from fastapi import APIRouter

router = APIRouter()


@router.get("/")
async def health_check():
    """Detailed health check endpoint"""
    return {
        "status": "healthy",
        "service": "robot-code-api",
        "version": "1.0.0",
        "details": {
            "database": "not_configured",
            "cache": "not_configured"
        }
    }