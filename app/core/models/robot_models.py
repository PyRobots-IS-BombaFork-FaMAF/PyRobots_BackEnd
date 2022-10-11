from typing import Optional
from unicodedata import name
from pydantic import BaseModel

class Robot(BaseModel):
    """
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    """
    name: str
    code: str
    avatar: Optional[str] = None

