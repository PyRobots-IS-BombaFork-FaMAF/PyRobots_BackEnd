from logging import Filter
from tokenize import String
from datetime import datetime, timedelta
from fastapi import *
from fastapi.responses import JSONResponse, HTMLResponse
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db 
from app.core.handlers.auth_handlers import *
from app.core.models.game_models import *
from app.core.game.partida import *

router = APIRouter()

@router.post("/game/create", status_code=201, tags=["Game"])
async def create_game(
    partida: PartidaIn,
    current_user: User = Depends(get_current_active_user)
):
    """
    Creates a game with the parameters passed, the game can
    be started later by the user who created it
    """
    PartidaObject(
        name=partida.name,
        rounds=partida.rounds,
        games=partida.games,
        max_players=partida.max_players,
        min_players=partida.min_players,
        creator=current_user["username"],
        player_robot={current_user["username"]: partida.robot},
        password=partida.password
    )
    msg = {"msg" : "Se creo la partida con éxito!"}
    return msg

@router.post("/game/list", status_code=200, tags=["Game"])
async def list_games(
    filtros: Filters, 
    current_user: User = Depends(get_current_active_user)
):
    """
    Returns a json with the data of the games created
    The filters are optional
    if only_private is set to true it will only show
    private games, if it's set to false it will show
    only public games, and if it's not set it will
    show all games.
    if created_by_user is set to true then it will only
    show games created by the current user
    the game_creation_date filters by day
    """
    if filtros.created_by_user:
        username = current_user["username"]
    else:
        username = None
    games = PartidaObject.filter_by(
        PartidaObject,
        datec=filtros.game_creation_date, 
        creator=username, 
        name=filtros.game_name,
        private=filtros.only_private
    )
    return games
