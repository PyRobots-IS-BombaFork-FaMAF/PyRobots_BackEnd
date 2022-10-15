from enum import unique
from pony.orm import *
from datetime import date, datetime
from passlib.context import CryptContext

db = Database()


class User(db.Entity):
    """
    Database table to store the user data, the 
    password stored corresponds to a has, the table
    uses the username column as a PK
    """
    username = PrimaryKey(str)
    email = Required(str, unique=True)
    password = Required(str, unique=False)
    avatar = Optional(str)
    validated = Required(bool, unique=False, default=0)
    robots = Set('Robot')
    created_games = Set('Partida')
    

class Robot(db.Entity):
    """
    Database table to store the robot data
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str, unique=True)
    code = Required(str)
    avatar = Optional(str)
    user = Required(User)


class Validation_data(db.Entity):
    """
    Database table to store the validation codes
    related to each email registered
    """
    email = PrimaryKey(str)
    code = Required(str)

class Partida(db.Entity):
    """
    Database table to store the parameters related
    to the games that still haven't been played in
    case of the server going down
    """
    id = PrimaryKey(int, auto=True)
    rounds = Required(int)
    games = Required(int)
    name = Required(str)
    max_players = Required(int)
    min_players = Required(int)
    created_by = Required(User)
    creation_date = Required(datetime)
    game_over = Required(bool, default=0)

def define_database_and_entities(**db_params):
    global db

    db.bind(**db_params)
    db.generate_mapping(create_tables=True)

    pass
