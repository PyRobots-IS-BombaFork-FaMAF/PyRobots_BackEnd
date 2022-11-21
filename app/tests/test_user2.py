from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User
from pony.orm import *
import json

IMAGEDIR = "app/avatars/"

client = TestClient(app_test)


def test_change_avatar():
    with open('app/avatars/avatar1.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"new_avatar": ("image_file", avatar_img, "image/jpeg")}
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffany123",
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
    response = client.put(
        "/user/avatar",
        headers={"accept": "test_application/json", "Authorization": head},
        files=avatar
    )
    assert response.status_code == 200

@db_session 
def test_verify_avatar(): 
    tiff = User["tiffbri"]
    assert tiff.avatar != IMAGEDIR + "default.jpg"

def test_invalid_avatar():
    with open('app/main.py', 'rb') as f:
        contents = f.read()
        f.close()
    file = {"new_avatar": ("avatar", contents, "images/jpeg")}
    response_login = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffany123",
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
    response = client.put(
        "/user/avatar",
        headers={"accept": "test_application/json", "Authorization": head},
        files=file
    )
    assert response.status_code == 409

def test_valid_change_password():
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffany123",
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
    payload = json.dumps({
        "old_password": "Tiffany123",
        "new_password": "Tiffanyb19!"
    })
    response= client.put(
        "/user/password", headers={"accept": "test_application/json", "Authorization": head},
        data=payload
    )
    assert response.status_code == 200

def test_login_with_new_pass(): 
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 200

def test_login_with_old_pass(): 
    response_login = client.post(
        "/token",
        data = {
            "grant_type": "",
            "username": "tiffbri",
            "password": "Tiffany123",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response_login.status_code == 401

def test_invalid_change_password1():
    response_login = client.post(
        "/token",
        data = {
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
    payload = json.dumps({
        "old_password": "Tiffanybric1!", #Wrong password
        "new_password": "Tiffany123"
    })
    response= client.put(
        "/user/password", headers={"accept": "test_application/json", "Authorization": head},
        data=payload
    )
    assert response.status_code == 401

def test_invalid_change_password2():
    response_login = client.post(
        "/token",
        data = {
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
    payload = json.dumps({
        "old_password": "Tiffanyb19!", 
        "new_password": "12345678" #No cumple restricciones
    })
    response= client.put(
        "/user/password", headers={"accept": "test_application/json", "Authorization": head},
        data=payload
    )
    assert response.status_code == 422