"""
Main API router for version 1
"""
from fastapi import APIRouter

from app.api.v1.endpoints import robots, health

api_router = APIRouter()

# Include endpoint routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(robots.router, prefix="/robots", tags=["robots"])