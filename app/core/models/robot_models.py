from typing import Optional
from typing_extensions import Required
from unicodedata import name
from pydantic import BaseModel, Field
from fastapi import *


class RobotIn(BaseModel):
    """
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    """
    name: str = Field(..., min_length=3, max_length=12)

    @classmethod
    def form(cls, name: str = Form(...)) -> 'RobotIn':
        return cls(name=name)


class Robot(BaseModel):
    """
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    """
    name: str
    code: str
    avatar: Optional[str] = None
