from asyncio.windows_events import NULL
from pony.orm import *
from datetime import date
from app.core.models.base import User, db
from app.core.models.base import define_database_and_entities

define_database_and_entities(
    provider='sqlite', filename='pyrobots-db.sqlite', create_db=True)

@db_session
def test_create_and_read_user():
    User(username="tiffb", email="tiff@gmail.com", password=User.hash_password("12345"))
    tiff = User["tiffb"]
    assert tiff.email == "tiff@gmail.com"

@db_session
def test_verify_password():
    tiff = User["tiffb"]
    assert User.verify_password(tiff, "12345") == True

@db_session
def test_update_password():
    tiff = User["tiffb"]
    tiff.password = User.hash_password("54321")
    flush()
    tiff = User["tiffb"]
    assert User.verify_password(tiff, "54321")  == True

@db_session
def test_delete_user():
    User["tiffb"].delete()
    try:
        tiff = User["tiffb"]
    except ObjectNotFound:
        tiff = NULL
    assert tiff == NULL