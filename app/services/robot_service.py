"""
Robot service for business logic
"""
from typing import List, Optional
from datetime import datetime, UTC

from app.schemas.robot import Robot, RobotCreate, RobotUpdate


class RobotService:
    """Service class for robot operations"""
    
    def __init__(self):
        # In-memory storage for demo purposes
        # In production, this would be replaced with database operations
        self._robots = {}
        self._next_id = 1
        
        # Add some sample data
        self._add_sample_data()
    
    def _add_sample_data(self):
        """Add sample robots for demonstration"""
        sample_robots = [
            RobotCreate(
                name="Atlas",
                model="Humanoid-v2",
                status="active",
                battery_level=85.5,
                location="Lab A"
            ),
            RobotCreate(
                name="Scout",
                model="Rover-X1",
                status="inactive",
                battery_level=32.0,
                location="Storage"
            )
        ]
        
        for robot_data in sample_robots:
            self.create_robot(robot_data)
    
    def get_all_robots(self) -> List[Robot]:
        """Get all robots"""
        return list(self._robots.values())
    
    def get_robot_by_id(self, robot_id: int) -> Optional[Robot]:
        """Get a robot by ID"""
        return self._robots.get(robot_id)
    
    def create_robot(self, robot_data: RobotCreate) -> Robot:
        """Create a new robot"""
        now = datetime.now(UTC)
        robot = Robot(
            id=self._next_id,
            **robot_data.model_dump(),
            created_at=now,
            updated_at=now
        )
        self._robots[self._next_id] = robot
        self._next_id += 1
        return robot
    
    def update_robot(self, robot_id: int, robot_update: RobotUpdate) -> Optional[Robot]:
        """Update an existing robot"""
        if robot_id not in self._robots:
            return None
        
        robot = self._robots[robot_id]
        update_data = robot_update.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            setattr(robot, field, value)
        
        robot.updated_at = datetime.now(UTC)
        return robot
    
    def delete_robot(self, robot_id: int) -> bool:
        """Delete a robot"""
        if robot_id in self._robots:
            del self._robots[robot_id]
            return True
        return False