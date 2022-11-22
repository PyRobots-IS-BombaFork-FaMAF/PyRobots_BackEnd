from pony.orm import *
from datetime import datetime

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
    results = Set('Results')
    
class Robot(db.Entity):
    """
    Database table to store the robot data
    """
    id = PrimaryKey(int, auto=True)
    name = Required(str)
    code = Required(str)
    avatar = Optional(str)
    user = Optional(User)
    results = Set('Results')
    composite_key(user, name)


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
    password = Optional(str)
    players = Required(Json)
    Results = Optional('Results')

class Results(db.Entity):
    """
    Database table to store the results from
    the multiplayer games
    """
    id = PrimaryKey(int, auto=True)
    partida = Required(Partida)
    winners = Set(User)
    robot_winners = Set(Robot)
    duration = Required(float)
    rounds_won = Required(int)

class RecoveryCode(db.Entity):
    """
    Database table to store the code for 
    password recoveries and the date it was 
    issued
    """
    username = PrimaryKey(str)
    code = Required(str)
    date_issue = Required(datetime)
    active = Required(bool, default=1)
class RobotStatistics(db.Entity):
    """
    Database table to store statistics
    the robots
    """
    robot_id = PrimaryKey(int, auto=False)
    gamesPlayed = Required(int, default=0)
    wins = Required(int, default=0)
    tied = Required(int, default=0)
    losses = Required(int, default=0)

def define_database_and_entities(**db_params):
    global db

    db.bind(**db_params)
    db.generate_mapping(create_tables=True)

@db_session
def load_default_robots():
    try:
        exists_circle = db.exists("select * from Robot where name = 'default_circle' and user is null")
        if not exists_circle:
            Robot(
                name = "default_circle",
                code = "app/tests/robots_for_testing/circle.py",
                avatar = "app/robot_avatars/default.jpg"
            )
        exists_scaa = db.exists("select * from Robot where name = 'default_scan_attack' and user is null")
        if not exists_scaa:
            Robot(
                name = "default_scan_attack",
                code = "app/tests/robots_for_testing/Scan_and_attack.py",
                avatar = "app/robot_avatars/default.jpg"
            )
    except:
        pass