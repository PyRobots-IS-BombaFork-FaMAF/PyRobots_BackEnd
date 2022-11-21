from pony.orm import *
from datetime import date
from app.core.models.base import User, db, Robot
from app.core.models.base import load_default_robots
from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.handlers.password_handlers import verify_password, hash_password

client = TestClient(app_test)


@db_session
def test_create_and_read_user():
    User(username="tiffb", email="tiff@gmail.com",
         password=hash_password("12345"))
    tiff = User["tiffb"]
    assert tiff.email == "tiff@gmail.com"


@db_session
def test_verify_password():
    tiff = User["tiffb"]
    assert verify_password(tiff.password, "12345") == True


@db_session
def test_update_password():
    tiff = User["tiffb"]
    tiff.password = hash_password("54321")
    flush()
    tiff = User["tiffb"]
    assert verify_password(tiff.password, "54321") == True


@db_session
def test_create_and_read_robot():
    tiff = User["tiffb"]
    Robot(name="Maximus", code="robot.py", user=tiff)
    flush()
    maximus = Robot[1]
    assert maximus.name == "Maximus"


@db_session
def test_update_code():
    maximus = Robot[1]
    maximus.code = "prueba.py"
    flush()
    maximus = Robot[1]
    assert maximus.code == "prueba.py"


@db_session
def test_delete_robot():
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

@db_session
def test_load_default_robots():
    load_default_robots()
    assert db.exists("select * from Robot where name = 'default_circle' and user is null")
    assert db.exists("select * from Robot where name = 'default_scan_attack' and user is null")

