from logging import Filter
from tokenize import String
from datetime import datetime, timedelta
from fastapi import *
from fastapi import WebSocket as ws
from fastapi.responses import JSONResponse, HTMLResponse
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db 
from app.core.handlers.auth_handlers import *
from app.core.handlers.password_handlers import *
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
    partida = PartidaObject(
        name=partida.name,
        rounds=partida.rounds,
        games=partida.games,
        max_players=partida.max_players,
        min_players=partida.min_players,
        creator=current_user["username"],
        player_robot={current_user["username"]: partida.robot},
        password=partida.password
    )
    msg = {"msg" : "Se creo la partida con éxito!", "WebSocket" : partida._websocketurl}
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
        datec=filtros.game_creation_date, 
        creator=username, 
        name=filtros.game_name,
        private=filtros.only_private
    )
    return games

@router.post("/game/{game_id}/join", status_code=200, tags=["Game"])
async def join_game(
    game: PartidaJoin,
    current_user: User = Depends(get_current_active_user)
):
    """
    Adds a user to an existing game
    """
    try:
        partida = PartidaObject.get_game_by_id(game.game_id)
    except:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    
    if partida == None:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    elif not partida.is_available():
        raise HTTPException(status_code=403, detail= "La partida ya está ejecutandose")
    elif not partida.can_join():
        raise HTTPException(status_code=403, detail= "Se alcanzó la cantidad máxima de jugadores")
    else:
        if partida._private and (game.password == None or not 
        verify_password(partida._password, game.password)):
            raise HTTPException(status_code=403, detail= "La contraseña es incorrecta")
        else:
            await partida.join_game(current_user["username"], game.robot)
    msg = {"msg" : "Te uniste a la partida con éxito!", "WebSocket": partida._websocketurl}
    return msg


@router.websocket("/game/lobby/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    try:
        partida = PartidaObject.get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    try:
        await partida._connections.connect(websocket)
    except RuntimeError:
        raise HTTPException(status_code=404, detail= "Error estableciendo conexión")
    while True:
        try:
            await websocket.receive()
        except RuntimeError:
            break