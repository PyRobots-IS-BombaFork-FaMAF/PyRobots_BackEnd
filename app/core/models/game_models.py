from ast import Str
from datetime import datetime
from operator import ge, le
from typing import Optional
from typing_extensions import Required
from unicodedata import name
from pydantic import BaseModel, Field, validator
from fastapi import *
from fastapi.exceptions import RequestValidationError, ValidationError

class PartidaIn(BaseModel):
    """
    BaseModel for the games, determines the data collected 
    to access the game endpoints
    """
    rounds: Optional[int] = Field(10000, ge=1, le=10000)
    games: Optional[int] = Field(200, ge=1, le=200)
    name: str = Field(..., min_length=3, max_length=12)
    max_players: Optional[int] = Field(4, ge=2, le=4)
    min_players: Optional[int] = Field(2, ge=2, le=4)

    @validator("min_players")
    def check_range(cls, v, values):
        if v > values["max_players"]:
            raise ValidationError('La cantidad máxima de jugadores no puede ser menor a la mínima')
        return v


class Filters(BaseModel):
    """
    BaseModel for the games filters, determines the game data
    that is returned to the user
    """
    game_name: Optional[str] = Field(None, min_length=3, max_length=12)
    game_creation_date: Optional[datetime] = None
    created_by_user: Optional[bool] = None