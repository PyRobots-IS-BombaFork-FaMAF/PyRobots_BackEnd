from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User, Validation_data, db, Robot
from pony.orm import *

client = TestClient(app_test)

def test_user_name():
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
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
    )
    assert response.status_code == 200
    assert response.headers["name"] == "tiffbri"
    

def test_user_name_and_email():
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "email": "tiffanybricett1281996@gmail.com",
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
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
    )
    assert response.status_code == 200
    assert response.headers["name"] == "tiffbri"
    assert response.headers["email"] == "tiffanybricett1281996@gmail.com"
    

    
def test_username_invalid():
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "email": "tiffanybricett1281996@gmail.com",
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
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
    )
    assert response.status_code == 200
    assert response.headers["email"] == "tiffanybricett1281996@gmail.com"
    assert response.headers["name"] != "diferentName"

def test_Unregistered_user():
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "germandddd",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 401

def test_user_avatar():
    pass  
    
