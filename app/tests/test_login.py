from fastapi.testclient import TestClient
from app.tests.test_main import app_test

client = TestClient(app_test)

def test_login_user_valid():
    response = client.post(
        "/token",
        data={
            "grant_type": "",
            "username": "tiffbr",
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
            "username": "tiffbr",
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
            "username": "tiffbr",
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
            "username": "tiffbr",
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
            "username": "tiffbr",
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