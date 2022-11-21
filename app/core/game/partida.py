from datetime import datetime
from app.core.models.base import *
from app.core.models.base import User as UserDB
from app.core.models.base import Robot as RobotDB
from app.core.models.base import RobotStatistics as RobotStatisticsDB
from app.core.handlers.password_handlers import *
from app.core.handlers.robot_handlers import *
from app.core.handlers.userdb_handlers import *
from app.core.game.game import *
from pony.orm import *
import json
import time
from fastapi import WebSocket
from typing import List
import asyncio
import base64

class PartidaObject():

    all = []

    @db_session
    def __init__(self, name, rounds, games, max_players, min_players, creator, player_robot,
                current_players=None, id=None, creation_date=None, fromdb=None, password=None):
        self._id = id
        self._name = name
        self._rounds = rounds
        self._games = games
        self._max_players = max_players
        self._min_players = min_players
        self._creator = creator
        self._players = [player_robot] if not fromdb else player_robot
        self._current_players = len(self._players)
        self._creation_date = (datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            if not creation_date else creation_date)
        self._password = "" if not password else (hash_password(password) if not fromdb else password)
        self._private = False if not password else True
        PartidaObject.all.append(self)
        self._gameStatus = 0
        self._connections = ConnectionManager()
        self._websocketurl = f"/game/lobby/{self._id}"
        if not fromdb:
            PartidaDB = Partida(
                rounds = rounds,
                games = games,
                name = name,
                max_players = max_players,
                min_players = min_players,
                created_by = creator,
                creation_date = self._creation_date,
                password = self._password,
                players = self._players
            )
            PartidaDB.flush()
            self._id = PartidaDB.id
            self._websocketurl = f"/game/lobby/{self._id}"

    @classmethod
    @db_session
    def init_from_db(cls):
        try:
            partidas = db.select("select * from Partida where game_over=0")[:]
        except Exception as err:
            partidas = []
        for partida in partidas:
            if partida.game_over != 1:
                game = PartidaObject(
                    id=partida.id,
                    name=partida.name,
                    rounds=partida.rounds,
                    games=partida.games,
                    max_players=partida.max_players,
                    min_players=partida.min_players,
                    player_robot=json.loads(partida.players),
                    current_players=len(json.loads(partida.players)),
                    creator=partida.created_by,
                    creation_date=partida.creation_date,
                    fromdb=True,
                    password=partida.password)

    @classmethod
    def filter_by(cls, datec=None, creator=None, name=None, private=None):
        partidas = [
            vars(x) for x in cls.all if
                (not datec
                or datetime.strptime(x._creation_date,"%Y-%m-%d %H:%M:%S.%f").date() == datec.date())
                and (not creator or x._creator.lower() == creator.lower())
                and (not name or x._name.lower() == name.lower())
                and (x._private == private if private!=None else not private)]
        result = json.dumps(partidas, default=lambda o: '<not serializable>', indent=4)
        return json.dumps(partidas, default=lambda o: '<not serializable>',
            sort_keys=True)

    @classmethod
    def get_game_by_id(cls, id):
        partida = None
        for x in cls.all:
            if x._id == id:
                partida = x
        return partida

    @db_session
    async def join_game(self, username, robotid):
        robot = RobotDB[robotid]
        if not any(d['player'] == username for d in self._players):
            self._players.append({'player': username, 'robot': robot.name})
        else:
            for d in self._players:
                if d['player'] == username:
                    d['robot'] = robot.name
        self._current_players = len(self._players)
        Partida[self._id].players = self._players
        db.flush()
        await self._connections.broadcast(
            f"¡El jugador {username} se ha unido a la partida!",
            self._players, 0
            )

    @db_session
    async def leave_game(self, username):
        for d in self._players:
            if d['player'] == username:
                self._players.remove(d)
                break
        self._current_players = len(self._players)
        Partida[self._id].players = self._players
        db.flush()
        await self._connections.broadcast(
            f"\n¡El jugador {username} ha abandonado la partida!",
            self._players, 1
        )

    @db_session
    def execute_game(self):
        self._gameStatus = 1
        robots_ingame = get_robot_inputs(self)
        list_of_inputs = [dict_player["input"] for dict_player in robots_ingame]
        start = time.time()
        for i in range(self._games):
            result = runSimulation(list_of_inputs, self._rounds)
            for index in result:
                dict_player = robots_ingame[index]
                dict_player["wins"] += 1
        self._gameStatus = 2
        duration = (time.time() - start) # Game duration in seconds
        Partida[self._id].game_over = 1
        db.flush()
        results = save_results(robots_ingame, duration, self._id)
        winners = [d["username"] for d in results]
        msg = f"¡La partida ha finalizado! "
        if len(winners) != 1:
            msg += f"Los ganadores son: " + str(winners)
        else:
            msg += f"El ganador es: " + str(winners)
        asyncio.run(self._connections.broadcast(
            msg,
            self._players, 3
            ))
        return winners

    def is_available(self):
        return self._gameStatus==0

    def can_join(self):
        return self._current_players < self._max_players

    def all_players(self):
        return self._current_players >= self._min_players

@db_session
def save_results(results, duration: int, id_game: int):
    sorted_winners = sorted(results, key=lambda x: x['wins'], reverse=True)
    max_winner = sorted_winners[0]
    max_wins = max_winner["wins"]
    winners = [dict_player for dict_player
        in sorted_winners if dict_player["wins"] == max_wins]
    
    for player in results:
        robot_id = get_robot_id(player["username"], player["input"].name)
        try:
            robot_Statistics = RobotStatisticsDB[robot_id]
        except:
            robot_Statistics = RobotStatisticsDB(
                robot_id = robot_id
            )
        robot_Statistics.gamesPlayed += 1
        if player in winners and len(winners) == 1:
            robot_Statistics.wins += 1
        elif player in winners and len(winners) > 1:
            robot_Statistics.tied += 1
        else:
            robot_Statistics.losses += 1
    
    Results(
        partida=id_game,
        winners= set(UserDB[dict_player["username"]] for dict_player in winners),
        robot_winners=set(
            RobotDB[get_robot_id(dict_player["username"], dict_player["input"].name)]
            for dict_player in winners),
        duration=duration,
        rounds_won=max_wins
    )
    return winners

@db_session
def get_robot_inputs(partida: PartidaObject):
    robots_ingame = []
    for player in partida._players:
            robot_db = RobotDB[get_robot_id(player['player'], player['robot'])]
            if robot_db.user != None:
                input = RobotInput(
                    pathToCode= robot_db.code.replace('/', '.')[:-3],
                    robotClassName=get_original_filename(player['player'],
                        robot_db.name, robot_db.code.rsplit('/', 1)[1])[:-3],
                    name=robot_db.name
                )
            else:
                pathToCode= robot_db.code.replace('/', '.')[:-3]
                input = RobotInput(
                    pathToCode= pathToCode,
                    robotClassName= pathToCode.rsplit('.', 1)[1],
                    name=robot_db.name
                )
            dict_player = {"input": input, "username": player["player"], "wins": 0}
            robots_ingame.append(dict_player)
    return robots_ingame

@db_session
def add_avatars(players):
    new_list = []
    for player in players:
        p = dict.copy(player)
        new_list.append(p)
    for player in new_list:
        user = UserDB[player["player"]]
        robot = RobotDB[get_robot_id(player["player"], player["robot"])]
        with open(user.avatar, 'rb') as f:
            avatar_img = base64.b64encode(f.read())
            f.close()
        with open(robot.avatar, 'rb') as f:
            robot_img = base64.b64encode(f.read())
            f.close()
        player["avatar_user_image"] = str(avatar_img)
        player["avatar_robot_image"] = str(robot_img)
        player["avatar_user_name"] = user.avatar.rsplit('/', 1)[1]
        player["avatar_robot_name"] = robot.avatar.rsplit('/', 1)[1]
    return new_list

class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def disconnect(self, websocket: WebSocket):
        await websocket.close()
        self.connections.remove(websocket)

    async def connect(self, websocket: WebSocket, players):
        await websocket.accept()
        await websocket.send_json(
            {"status": 4,
            "message": "Bienvenido a la partida",
            "players": add_avatars(players)}
            )
        self.connections.append(websocket)

    async def broadcast(self, data: str, players, status):
        """
        status: 0 - Someone joined the game
        status: 1 - Someone left the game
        status: 2 - The game has started
        status: 3 - The game has finished
        status: 4 - Welcome to the game (Not broadcasted, only sent to one websocket)
        """
        for connection in self.connections:
            try:
                await connection.send_json(
                    {"status": status,
                    "message": data,
                    "players": add_avatars(players)}
                )
            except:
                self.connections.remove(connection)
