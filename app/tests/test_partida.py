from calendar import c
from datetime import datetime
from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User, Validation_data, db, Robot
from pony.orm import *
import json
from urllib.parse import quote
from app.core.game.partida import *
from pony.orm import *
import pytest

client = TestClient(app_test)

def test_create_valid_partida_sin_pass1():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 10000,
            "games": 200,
            "name": "Exacto",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201

def test_create_valid_partida_con_pass():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 10000,
            "games": 200,
            "name": "string",
            "max_players": 4,
            "min_players": 2,
            "password": "Tiffany123",
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201


def test_create_valid_partida_default_rounds():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "games": 200,
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201


def test_create_valid_partida_default_games():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201


def test_create_valid_partida_default_max_players():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "name": "Prueba1",
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201


def test_create_valid_partida_default_min_players():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "name": "Prueba1",
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 201


def test_create_valid_partida_invalid_rounds1():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 0, # rounds < 1
            "games": 10000,
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422


def test_create_valid_partida_invalid_rounds2():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 100000, # rounds > 10000
            "games": 10000,
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422


def test_create_valid_partida_invalid_games1():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 100,
            "games": 0, # games < 1
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422

def test_create_valid_partida_invalid_games2():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 100, 
            "games": 1000, # games > 200
            "name": "Prueba1",
            "max_players": 4,
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422

def test_create_valid_partida_invalid_max_players1():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 100, 
            "games": 200, 
            "name": "Prueba1",
            "max_players": 1, # max_player < 2
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422

def test_create_invalid_players():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
            "rounds": 100, 
            "games": 200, 
            "name": "Prueba1",
            "max_players": 3, # min_player > max_player
            "min_players": 4,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422

def test_create_partida_without_login():
    body = {
            "rounds": 100, 
            "games": 200, 
            "name": "Prueba1",
            "max_players": 4, # min_player > max_player
            "min_players": 2,
            "robot": "Maximus"
        }
    response = client.post(
        "/game/create",
        headers={"accept": "test_application/json"},
        json=body
    )
    assert response.status_code == 401

def test_listar_todas_partidas():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        }
    response = client.post(
        "/game/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    data = json.loads(tmp_list)
    assert response.status_code == 200 and len(data) == 6

def test_listar_partidas_por_fecha():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "game_creation_date": str(datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        }
    response = client.post(
        "/game/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    data = json.loads(tmp_list)
    assert response.status_code == 200 and len(data) == 6

def test_listar_solo_partidas_publicas():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "only_private": False
        }
    response = client.post(
        "/game/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    data = json.loads(tmp_list)
    assert response.status_code == 200 and len(data) == 5

def test_listar_solo_partidas_privadas():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "only_private": True
        }
    response = client.post(
        "/game/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    data = json.loads(tmp_list)
    assert response.status_code == 200 and len(data) == 1

def test_listar_solo_partidas_de_user():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "created_by_user": True
        }
    response = client.post(
        "/game/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    data = json.loads(tmp_list)
    assert response.status_code == 200 and len(data) == 6

def test_register_valid_user_without_avatar():
    response = client.post("users/register",
                           data={
                               "username": "tiffbr19",
                               "email": "tiffanybricett199625@hotmail.com",
                               "password": "Tiffanyb19!"
                           }
                           )
    assert response.status_code == 201

@db_session
def test_validate_user():
    email = "tiffanybricett199625@hotmail.com"
    validation_tuple = db.get(
        "select * from validation_data where email = $email")
    code = validation_tuple[1]
    url = "/validate?email="+quote(email)+"&code="+code
    response = client.get(url)
    assert response.status_code == 200


def test_unirse_a_partida_sin_pass():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "game_id": 1,
        "robot": "Felipe"
        }
    response = client.post(
        "/game/1/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    print(response.json())
    assert response.status_code == 200 

def test_unirse_a_partida_con_pass():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "game_id": 2,
        "robot": "Felipe",
        "password": "Tiffany123"
        }
    response = client.post(
        "/game/2/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 200 

def test_unirse_a_partida_con_pass_invalido():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "game_id": 2,
        "robot": "Felipe",
        "password": "12345678"
        }
    response = client.post(
        "/game/2/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 403

def test_unirse_a_partida_sin_robot():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    body = {
        "game_id": 2
        }
    response = client.post(
        "/game/2/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422

def test_unirse_a_partida_llena():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    partida = PartidaObject.get_game_by_id(1)
    partida._current_players = 4
    body = {
        "game_id": 1,
        "robot": "Felipe"
        }
    response = client.post(
        "/game/2/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 403

def test_unirse_a_partida_en_curso():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr19",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200
    rta: dict = response_login.json()
    token: str = rta["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    partida = PartidaObject.get_game_by_id(1)
    partida._gameStatus = 1
    body = {
        "game_id": 1,
        "robot": "Felipe"
        }
    response = client.post(
        "/game/2/join",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 403

def test_websocket():
    with client.websocket_connect("/game/lobby/1") as websocket:
        data = websocket.receive_text()
        assert data == "Bienvenido a la partida"