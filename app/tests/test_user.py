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
    body = {
        }
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_user = response.json()
    assert response.status_code == 200
    assert len(tmp_user) == 3
    assert tmp_user["name"] == "tiffbri"
    

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
    body = {
        }
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_user = response.json()
    assert response.status_code == 200
    assert len(tmp_user) == 3
    assert tmp_user["name"] == "tiffbri"
    assert tmp_user["email"] == "tiffanybricett1281996@gmail.com"
    

    
def test_user_avatar():
    pass
