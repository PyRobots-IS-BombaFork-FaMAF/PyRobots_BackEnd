from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import *


class RobotIn(BaseModel):
    """
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    """
    name: str = Field(..., min_length=3, max_length=12)

    @validator('*', pre=True)
    def remove_blank_strings(cls, v):
        """Removes whitespace characters and return None if empty"""
        if isinstance(v, str):
            v = v.strip()
        if v == "":
            return None
        return v
    
    @classmethod
    def form(cls, name: str = Form(...)) -> 'RobotIn':
        return cls(name=name)


class Robot(BaseModel):
    """
    BaseModel for the robot, determines the data collected 
    to access the robot endpoints
    """
    name: str
    code: str
    avatar: Optional[str] = None


class RobotSimulation(BaseModel):
    """
    BaseModel for the robot, determines the data collected 
    to access the robot endpoints
    """
    
    id: int
    