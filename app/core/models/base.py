from pony.orm import *
from datetime import date
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

class Validation_data(db.Entity):
    """
    Database table to store the validation codes
    related to each email registered
    """
    email = PrimaryKey(str)
    code = Required(str)


def define_database_and_entities(**db_params):
    global db

    db.bind(**db_params)
    db.generate_mapping(create_tables=True)

    pass