from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, validator
from fastapi import *
from fastapi.exceptions import ValidationError

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
    password: str = Field(None, min_length=8, max_length=16)
    robot: int

    @validator("min_players")
    def check_range(cls, v, values):
        if "max_players" in values and v > values["max_players"]:
            raise ValidationError('La cantidad máxima de jugadores no puede ser menor a la mínima')
        return v

    @validator('*', pre=True)
    def remove_blank_strings(cls, v):
        """Removes whitespace characters and return None if empty"""
        if isinstance(v, str):
            v = v.strip()
        if v == "":
            return None
        return v


class Filters(BaseModel):
    """
    BaseModel for the games filters, determines the game data
    that is returned to the user
    if only_private = None shows all games
    if only_private = True shows only private games
    if only_private = False shows only public games
    """
    game_name: Optional[str] = Field(None, min_length=3, max_length=12)
    game_creation_date: Optional[datetime] = None
    created_by_user: Optional[bool] = None
    only_private: Optional[bool] = None



class SimulationIn(BaseModel):
    """
    BaseModel for the simulation, determines the data collected 
    to access the simulation endpoints
    """
    
    rounds: Optional[int] = Field(10000, ge=1, le=10000)

class PartidaJoin(BaseModel):
    """
    BaseModel for the data received when an user is trying to join
    a game
    """
    game_id: int
    robot: int
    password: Optional[str] = Field(None)
