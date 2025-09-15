"""
Robot schemas for request/response models
"""
from typing import Optional
from pydantic import BaseModel, Field
from datetime import datetime


class RobotBase(BaseModel):
    """Base robot schema"""
    name: str = Field(..., description="Robot name", min_length=1, max_length=100)
    model: str = Field(..., description="Robot model", min_length=1, max_length=50)
    status: str = Field(default="inactive", description="Robot status (active/inactive/maintenance)")
    battery_level: Optional[float] = Field(None, description="Battery level (0-100)", ge=0, le=100)
    location: Optional[str] = Field(None, description="Current robot location", max_length=200)


class RobotCreate(RobotBase):
    """Schema for creating a new robot"""
    pass


class RobotUpdate(BaseModel):
    """Schema for updating an existing robot"""
    name: Optional[str] = Field(None, description="Robot name", min_length=1, max_length=100)
    model: Optional[str] = Field(None, description="Robot model", min_length=1, max_length=50)
    status: Optional[str] = Field(None, description="Robot status (active/inactive/maintenance)")
    battery_level: Optional[float] = Field(None, description="Battery level (0-100)", ge=0, le=100)
    location: Optional[str] = Field(None, description="Current robot location", max_length=200)


class Robot(RobotBase):
    """Full robot schema with ID and timestamps"""
    id: int = Field(..., description="Robot ID")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: datetime = Field(..., description="Last update timestamp")
    
    model_config = {"from_attributes": True}