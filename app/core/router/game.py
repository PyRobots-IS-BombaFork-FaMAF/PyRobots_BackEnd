from fastapi import *
from fastapi.responses import JSONResponse
from app.core.models.base import db 
from app.core.models.base import User as UserDB
from app.core.models.base import Robot as RobotDB
from app.core.handlers.auth_handlers import *
from app.core.handlers.robot_handlers import *
from app.core.handlers.password_handlers import *
from app.core.models.game_models import *
from app.core.models.robot_models import *
from app.core.game.partida import *
from app.core.game.game import *

router = APIRouter()

@router.post("/game/create", status_code=201, tags=["Game"])
@db_session
def create_game(
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
        player_robot={'player': current_user["username"], 'robot': RobotDB[partida.robot].name},
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

@router.post("/simulation", status_code=200, tags=["Game"])
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
            allRobotsUser = db.select("select * from Robot where (user = $uname or user is null) and id = $robot.id")
            if(allRobotsUser == []):
                raise HTTPException(400, detail="robot invalido")
            listRobots.append(allRobotsUser)
    else: 
        raise HTTPException(400, detail="Cantidad de robots invalida")
    for bot in listRobots:
        pathCodeRobot = bot[0].code.replace('/', '.')[:-3]
        if bot[0].user != None:
            robotInputs.append(RobotInput(pathCodeRobot, 
                                        get_original_filename(uname, bot[0].name, bot[0].code.rsplit('/', 1)[1])[:-3], 
                                        bot[0].name))
        else:
            robotInputs.append(RobotInput(pathCodeRobot, pathCodeRobot.rsplit('.', 1)[1], bot[0].name))
    resultSimulation = runSimulation(robotInputs, rounds.rounds, True).json_output()

    return JSONResponse(resultSimulation)


@router.post("/game/{game_id}/join", status_code=200, tags=["Game"])
async def join_game(
    game: PartidaJoin,
    current_user: User = Depends(get_current_active_user)
):
    """
    Adds an user to an existing game
    """
    try:
        partida = PartidaObject.get_game_by_id(game.game_id)
    except:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    
    if partida == None:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    elif not partida.is_available():
        if partida._gameStatus == 1:
            raise HTTPException(status_code=403, detail= "La partida ya está ejecutandose")
        else:
            raise HTTPException(status_code=403, detail= "La partida ya ha finalizado")
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

@router.get("/game/{game_id}/start", status_code=200, tags=["Game"])
async def start_game(
    game_id: int,
    current_user: User = Depends(get_current_active_user),
    background_t: BackgroundTasks = BackgroundTasks()
):
    """
    Endpoint to start a game
    """
    try:
        partida = PartidaObject.get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail= "Partida inexistente")

    if partida == None:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    elif (current_user["username"] != partida._creator):
        raise HTTPException(status_code=403, 
            detail= "La partida solo puede ser iniciada por el creador de la misma")
    elif not partida.is_available():
        if partida._gameStatus == 1:
            raise HTTPException(status_code=403, detail= "La partida ya está ejecutandose")
        else:
            raise HTTPException(status_code=403, detail= "La partida ya ha finalizado")
    elif not partida.all_players():
        raise HTTPException(status_code=403, 
            detail= f"Se necesitan mínimo {partida._min_players} para iniciar la partida")
    else:
        msg = f"¡La partida se esta iniciando! Esperando resultados.."
        await partida._connections.broadcast(
            msg,
            partida._players, 2)
        background_t.add_task(partida.execute_game)
        
    msg = {"message": "La partida ha finalizado"}

    return msg

@router.get("/game/results")
@db_session
def get_player_results(
    current_user: User = Depends(get_current_active_user)
):
    """
    Endpoint to get a list of the results of every game
    the user has played
    """
    username = current_user["username"]
    #getting all finished games
    try:
        games_played = list(Partida.select().filter(lambda p: p.game_over == 1)[:])
    except:
        return {"msg": "No hay resultados"}
    
    results_list = []
    if games_played != []:
        game_copy = games_played.copy()
        for game in games_played:
            #filtering the games where the player played
            if not any(d['player'] == username.lower() for d in game.players):
                game_copy.remove(game)
        #getting the results from the games where the player played
        results = list(Results.select().filter(lambda r: r.partida in game_copy))
        if game_copy != None:
            for i in range(len(game_copy)):
                game = list(game_copy)[i]
                for result in results:
                    if result.partida == game:
                        game_result = result
                        break
                #getting users and robots from results set
                winners = list(UserDB.select().filter(lambda u: u in game_result.winners))
                robots = list(RobotDB.select().filter(lambda u: u in game_result.robot_winners))
                user_robot = []
                #matching robots to their owner
                for i in range(len(winners)):
                    uname = winners[i].username
                    for players in game.players:
                        if players["player"] == uname:
                            robot_name = players["robot"]
                            break
                    user_robot.append({'player': uname, 'robot': robot_name})
                result_dict = {
                    "id": game.id,
                    "name": game.name,
                    "creation_date": game.creation_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
                    "creator": game.created_by.username,
                    "rounds": game.rounds,
                    "games": game.games,
                    "is_private": False if not game.password else True,
                    "players": game.players,
                    "duration": game_result.duration,
                    "winners": user_robot,
                    "games_won": game_result.rounds_won
                }
                results_list.append(result_dict)
    return JSONResponse(results_list)


@router.websocket("/game/lobby/{game_id}")
async def websocket_endpoint(websocket: WebSocket, game_id: int):
    try:
        partida = PartidaObject.get_game_by_id(game_id)
    except:
        raise "Partida inexistente"
    if partida == None:
        return "Partida inexistente"
    try:
        await partida._connections.connect(websocket, partida._players)
    except:
        raise "Error estableciendo conexión"
    try:
        while True:
            await websocket.receive()
    except:
        pass


@router.post("/game/{game_id}/leave", status_code=200, tags=["Game"])
async def leave_game(
    game_id: int,
    current_user: User = Depends(get_current_active_user)
):
    """
    Remove an user to an existing game
    """
    try:
        partida = PartidaObject.get_game_by_id(game_id)
    except:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    if partida == None:
        raise HTTPException(status_code=404, detail= "Partida inexistente")
    elif (current_user["username"] == partida._creator):
        raise HTTPException(status_code=403, 
            detail= "El creador no puede abandonar la partida")
    elif not partida.is_available():
        if partida._gameStatus == 1:
            raise HTTPException(status_code=403, detail= "La partida ya está ejecutandose y no puede ser abandonada")
        else:
            raise HTTPException(status_code=403, detail= "La partida ya ha finalizado")
    else: 
        await partida.leave_game(current_user["username"])

    msg = {"msg" : "Abandonaste la partida con éxito!"}
    return msg
