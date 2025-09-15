"""
Robot-related API endpoints
"""
from typing import List
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.schemas.robot import Robot, RobotCreate, RobotUpdate
from app.services.robot_service import RobotService

router = APIRouter()
robot_service = RobotService()


@router.get("/", response_model=List[Robot])
async def get_robots():
    """Get all robots"""
    return robot_service.get_all_robots()


@router.get("/{robot_id}", response_model=Robot)
async def get_robot(robot_id: int):
    """Get a specific robot by ID"""
    robot = robot_service.get_robot_by_id(robot_id)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot


@router.post("/", response_model=Robot)
async def create_robot(robot: RobotCreate):
    """Create a new robot"""
    return robot_service.create_robot(robot)


@router.put("/{robot_id}", response_model=Robot)
async def update_robot(robot_id: int, robot_update: RobotUpdate):
    """Update an existing robot"""
    robot = robot_service.update_robot(robot_id, robot_update)
    if not robot:
        raise HTTPException(status_code=404, detail="Robot not found")
    return robot


@router.delete("/{robot_id}")
async def delete_robot(robot_id: int):
    """Delete a robot"""
    if not robot_service.delete_robot(robot_id):
        raise HTTPException(status_code=404, detail="Robot not found")
    return {"message": "Robot deleted successfully"}