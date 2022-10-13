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
    Partida(
        partida.name,
        partida.rounds,
        partida.games,
        partida.max_players,
        partida.min_players,
        current_user["username"]
    )
    msg = {"msg" : "Se creo la partida con éxito!"}
    return msg



