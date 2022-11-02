from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User, Validation_data, db, Robot
from pony.orm import *

from urllib.parse import quote
from pony.orm import *

client = TestClient(app_test)


def test_create_valid_robot_without_avatar():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents,
                          "application/x-python-code")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot1"
        },
        files=code_file
    )
    assert response.status_code == 201


def test_create_valid_robot_with_avatar():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents, "application/x-python-code"),
                 "avatar": ("avatar", avatar_img, "image/jpeg")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot2"
        },
        files=code_file
    )
    assert response.status_code == 201


def test_create_invalid_robot_name1():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents, "application/x-python-code"),
                 "avatar": ("avatar", avatar_img, "images/jpeg")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Ro"  # length < 3
        },
        files=code_file
    )
    assert response.status_code == 422


def test_create_invalid_robot_name2():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents, "application/x-python-code"),
                 "avatar": ("avatar", avatar_img, "images/jpeg")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Roejfu188jd8829a"  # length > 12
        },
        files=code_file
    )
    assert response.status_code == 422


def test_create_invalid_avatar_type():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents, "application/x-python-code"),
                 "avatar": ("avatar", code_contents, "images/jpeg")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot17"
        },
        files=code_file
    )
    assert response.status_code == 409


def test_create_invalid_code_type():
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    code_file = {"code": ("code.py", avatar_img, "image/jpeg")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot1"
        },
        files=code_file
    )
    assert response.status_code == 409


def test_create_existing_robot():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    code_file = {"code": ("code.py", code_contents,
                          "application/x-python-code")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot1"
        },
        files=code_file
    )
    assert response.status_code == 409


def test_create_without_code():
    with open('app/main.py', 'rb') as f:
        code_contents = f.read()
        f.close()
    code_file = {"code": ("", code_contents, "application/x-python-code")}
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
    response = client.post(
        "/robots/create",
        headers={"accept": "test_application/json", "Authorization": head},
        data={
            "name": "Robot178"
        },
        files=code_file
    )
    assert response.status_code == 400


def test_create_nonexistent_avatar():
    pass


def test_create_nonexistent_code():
    pass


def test_list_all_robots():
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
        "/robot/list",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_list = response.json()
    assert response.status_code == 200 and len(tmp_list) == 4