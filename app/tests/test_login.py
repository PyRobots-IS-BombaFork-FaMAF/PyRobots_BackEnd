from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import db
from urllib.parse import quote
from pony.orm import *

client = TestClient(app_test)


def test_register_valid_user_with_avatar():
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"avatar": ("image_file", avatar_img, "image/jpeg")}
    response = client.post("users/register",
                           data={
                               "username": "tiffbri",
                               "email": "tiffanybricett1281996@gmail.com",
                               "password": "Tiffanyb19!"
                           },
                           files=avatar
                           )
    assert response.status_code == 201


def test_login_and_get_non_validated_user():
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
    assert response_login.status_code == 401

@db_session
def test_validate_user_wrong_code():
    email = "tiffanybricett1281996@gmail.com"
    code = "Ai992kjHsnwh"
    url = "/validate?email="+quote(email)+"&code="+code
    response = client.get(url)
    assert response.status_code == 409


@db_session
def test_validate_user():
    email = "tiffanybricett1281996@gmail.com"
    validation_tuple = db.get(
        "select * from validation_data where email = $email")
    code = validation_tuple[1]
    url = "/validate?email="+quote(email)+"&code="+code
    response = client.get(url)
    assert response.status_code == 200


def test_validate_non_registered_user():
    email = "user@gmail.com"
    code = "A820akkHWhnd"
    url = "/validate?email="+quote(email)+"&code="+code
    response = client.get(url)
    assert response.status_code == 404


def test_login_user_valid():
    response = client.post(
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
    assert response.status_code == 200


def test_login_user_wrong_username():
    response = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "player",
            "password": "Tiffanyb19!",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Contraseña o usuario incorrecto"}


def test_login_user_wrong_pass():
    response = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbri",
            "password": "Wrong11235",
            "scope": "",
            "client_id": "",
            "client_secret": "",
        },
    )
    assert response.status_code == 401
    assert response.json() == {"detail": "Contraseña o usuario incorrecto"}


def test_invalid_token_user():
    response = client.get(
        "/users/me",
        headers={"accept": "test_application/json",
                 "Authorization": "Bearer a.bad.token"},
    )
    assert response.status_code == 401


def test_login_and_token_user():
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
    response: dict = response_login.json()
    token: str = response["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    response_token = client.get(
        "/users/me", headers={"accept": "test_application/json", "Authorization": head}
    )
    assert response_token.status_code == 200


def test_login_and_refresh_token():
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
    response: dict = response_login.json()
    token: str = response["access_token"]
    token_type: str = "Bearer "
    head: str = token_type + token
    response_token = client.put(
        "/users/refresh", headers={"accept": "test_application/json", "Authorization": head}
    )
    assert response_token.status_code == 201


def test_login_and_get():
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
    response_get = client.get(
        "/users/me", headers={"accept": "test_application/json", "Authorization": head}
    )
    assert response_get.status_code == 200


def test_logout():
    response = client.get("/logout")
    assert response.status_code == 401
