from datetime import date, datetime
from app.core.models.base import Partida, db 
from app.core.handlers.password_handlers import *
from pony.orm import *
import json
from fastapi import WebSocket
from typing import List

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
    async def join_game(self, username, robot):
        if not any(d['player'] == username for d in self._players):
            self._players.append({'player': username, 'robot': robot})
        else:
            for d in self._players:
                if d['player'] == username:
                    d['robot'] = robot
        self._current_players = len(self._players)
        Partida[self._id].players = self._players 
        db.flush()
        await self._connections.broadcast(f"\n¡El jugador {username} se ha unido a la partida!")

    def is_available(self):
        return self._gameStatus==0

    def can_join(self):
        return self._current_players < self._max_players


class ConnectionManager:
    def __init__(self):
        self.connections: List[WebSocket] = []

    async def desconnect(self, websocket: WebSocket):
        await websocket.close()
        self.connections.remove(websocket)

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        await websocket.send_text("Bienvenido a la partida")
        self.connections.append(websocket)

    async def broadcast(self, data: str):
        for connection in self.connections:
            try:
                await connection.send_text(data)
            except:
                self.connections.remove(connection)