from calendar import c
from datetime import datetime
from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User, Validation_data, db, Robot
from pony.orm import *
import json
from urllib.parse import quote
from pony.orm import *

client = TestClient(app_test)


def test_create_valid_partida_sin_pass():
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
            "min_players": 2
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
            "password": "Tiffany123"
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
            "min_players": 2
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
            "min_players": 2
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
            "min_players": 2
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
            "name": "Prueba1"
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
            "min_players": 2
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
            "min_players": 2
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
            "min_players": 2
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
            "min_players": 2
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
            "min_players": 2
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
            "min_players": 4
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
            "min_players": 2
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
    assert response.status_code == 200 and len(tmp_list) == 6

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
    assert response.status_code == 200 and len(tmp_list) == 6

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
    assert response.status_code == 200 and len(tmp_list) == 5

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
    assert response.status_code == 200 and len(tmp_list) == 1

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
    assert response.status_code == 200 and len(tmp_list) == 6