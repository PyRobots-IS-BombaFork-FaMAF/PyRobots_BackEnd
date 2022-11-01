from logging import Filter
from tokenize import String
from datetime import datetime, timedelta
from fastapi import *
from fastapi.responses import JSONResponse, HTMLResponse
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db 
from app.core.handlers.auth_handlers import *
from app.core.handlers.robot_handlers import *
from app.core.models.game_models import *
from app.core.models.robot_models import *
from app.core.game.partida import *
from app.core.game.game import *
import pathlib

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
        partida.name,
        partida.rounds,
        partida.games,
        partida.max_players,
        partida.min_players,
        current_user["username"],
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
        filtros.game_creation_date, 
        username, 
        filtros.game_name,
        filtros.only_private
    )
    return games

@router.post("/simulation", status_code=201, tags=["Game"])
@db_session
def simulation( 
    robots: list[RobotSimulation],
    rounds: SimulationIn,
    current_user: User = Depends(get_current_active_user)
):
    """
    run the simulation and return the results of the simulation
    """
    uname = current_user["username"]
    listRobots = []
    robotInputs = []
    if(len(robots) >= 2 and len(robots) <= 4):
        for robot in robots:
            allRobotsUser = db.select("select * from Robot where user = $uname and id = $robot.id")
            listRobots.append(allRobotsUser)
    else: 
        raise HTTPException(400, detail="Cantidad de robots invalida")
    for bot in listRobots:
        path = pathlib.Path(bot[0].code)
        print(path)
        formatted_path = '.'.join(path.with_suffix('').parts)
        robotInputs.append(RobotInput(formatted_path, 
                                    get_original_filename(current_user, 
                                                        bot[0].name, 
                                                        bot[0].code.rsplit('/', 1)[1]
                                                        ).rsplit('.', 1)[0], 
                                    bot[0].name))
    resultSimulation = runSimulation(robotInputs, rounds.rounds, True).json_output()

    return JSONResponse(resultSimulation)
    

