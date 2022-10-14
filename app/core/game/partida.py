from datetime import date, datetime
from app.core.models.base import Partida, db 
from pony.orm import *
import json

class PartidaObject():

    all = []

    @db_session
    def __init__(self, name, rounds, games, max_players, min_players, creator, creation_date=None):
        self._name = name
        self._rounds = rounds
        self._games = games 
        self._max_players = max_players
        self._min_players = min_players
        self._creator = creator
        self._creation_date = datetime.now().strftime("%Y/%m/%d %H:%M:%S") if not creation_date else creation_date
        self.all.append(self)
        Partida(
            rounds = rounds,
            games = games,
            name = name,
            max_players = max_players,
            min_players = min_players,
            created_by = creator,
            creation_date = self._creation_date
        )

    def partida_json(self):
        return self.__dict__

    @db_session
    def init_from_db(self):
        try:
            partidas = db.select("select * from Partida where game_over=0")[:]
        except Exception as err:
            partidas = []
        for partida in partidas:
            game = PartidaObject(
                partida.name,
                partida.rounds,
                partida.games,
                partida.max_players,
                partida.min_players,
                partida.created_by,
                partida.creation_date)




