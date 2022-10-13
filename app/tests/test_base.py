from pony.orm import *
from datetime import date
from app.core.models.base import User, db, Robot
from app.core.models.base import define_database_and_entities
from app.core.handlers.password_handlers import verify_password, hash_password

define_database_and_entities(
    provider='sqlite', filename='pyrobots-db.sqlite', create_db=True)

@db_session
def test_create_and_read_user():
    User(username="tiffb", email="tiff@gmail.com", password=hash_password("12345"))
    tiff = User["tiffb"]
    assert tiff.email == "tiff@gmail.com"

@db_session
def test_verify_password():
    tiff = User["tiffb"]
    assert verify_password(tiff, "12345") == True

@db_session
def test_update_password():
    tiff = User["tiffb"]
    tiff.password = hash_password("54321")
    flush()
    tiff = User["tiffb"]
    assert verify_password(tiff, "54321")  == True

@db_session
def create_and_read_robot():
    tiff = User["tiffb"]
    Robot(name="Maximus", code="robot.py", user=tiff)
    maximus = Robot[1]
    assert maximus.name == "Maximus"

@db_session
def update_code():
    maximus = Robot[1]
    maximus.code = "prueba.py"
    flush()
    maximus = Robot[1]
    assert maximus.code == "prueba.py"

@db_session
def delete_robot():
    Robot[1].delete()
    try:
        maximus = Robot[1]
    except ObjectNotFound:
        maximus = None
    assert maximus == None
    
@db_session
def test_delete_user():
    User["tiffb"].delete()
    try:
        tiff = User["tiffb"]
    except ObjectNotFound:
        tiff = None 
    assert tiff == None