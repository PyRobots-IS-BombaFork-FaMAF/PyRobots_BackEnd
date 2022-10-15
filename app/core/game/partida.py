from datetime import date, datetime
import json

class Partida():

    all = []

    def __init__(self, name, rounds, games, max_players, min_players, creator):
        self._name = name
        self._rounds = rounds
        self._games = games 
        self._max_players = max_players
        self._min_players = min_players
        self._creator = creator 
        self._creation_date = date.today().strftime("%d/%m/%Y")
        self.all.append(self)

    def partida_json(self):
        return self.__dict__



