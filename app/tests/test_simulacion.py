from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from pony.orm import *
from pony.orm import *

client = TestClient(app_test)

def test_create_simulation():
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
            "robots": [
                {
                "id": 2
                },
                {
                "id": 3
                }
            ],
            "rounds": {
                "rounds": 1000
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 200

def test_create_simulation_invalid_robots():
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
            "robots": [
                {
                "id": 0
                },
                {
                "id": 0
                }
            ],
            "rounds": {
                "rounds": 1000
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 400

def test_create_simulation_invalid_number_robots():
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
            "robots": [
                {
                "id": 2
                }
            ],
            "rounds": {
                "rounds": 1000
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 400

def test_create_simulation_overflow_number_robots():
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
            "robots": [
                {
                "id": 2
                },
                {
                "id": 2
                },
                {
                "id": 2
                },
                {
                "id": 2
                },
                {
                "id": 2
                }
            ],
            "rounds": {
                "rounds": 1000
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 400


def test_create_simulation_empty_number_robots():
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
            "robots": [],
            "rounds": {
                "rounds": 1000
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 400


def test_create_simulation_invalid_number_rounds():
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
            "robots": [
                {
                "id": 2
                },
                {
                "id": 3
                }
            ],
            "rounds": {
                "rounds": 10001
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422
    

def test_create_simulation_negative_number_rounds():
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
            "robots": [
                {
                "id": 2
                },
                {
                "id": 3
                }
            ],
            "rounds": {
                "rounds": -1
            }    
        }
    response = client.post(
        "/simulation",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    assert response.status_code == 422