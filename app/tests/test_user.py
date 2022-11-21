from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import db
from datetime import datetime, timedelta
import json
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
    assert tmp_user["name"] == "tiffbri"
    assert tmp_user["email"] == "tiffanybricett1281996@gmail.com"

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
    body = {
        }
    response = client.get(
        "/user/info",
        headers={"accept": "test_application/json", "Authorization": head},
        json=body
    )
    tmp_user = response.json()
    assert response.status_code == 200
    assert tmp_user["name"] != "diferentName"

def test_send_code():
    response = client.get("/pass-recovery?username=tiffbri")
    assert response.status_code == 200

@db_session
def test_new_pass_invalid_user():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    payload = json.dumps({
        "username": "tiffany",
        "code": code,
        "password": "Tiffany123"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 403

@db_session
def test_new_pass_invalid_code():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    payload = json.dumps({
        "username": "tiffbri",
        "code": "AKkdmmsju8",
        "password": "Tiffany123"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 403

@db_session
def test_new_pass_invalid_pass():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    payload = json.dumps({
        "username": "tiffbri",
        "code": code,
        "password": "12345"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 422

@db_session
def test_new_pass_expired():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    recovery.date_issue = datetime.now() - timedelta(days=2)
    db.flush()  
    payload = json.dumps({
        "username": "tiffbri",
        "code": code,
        "password": "Tiffany123"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 403

@db_session
def test_new_pass():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    recovery.date_issue = datetime.now() 
    payload = json.dumps({
        "username": "tiffbri",
        "code": code,
        "password": "Tiffany123"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 200

def test_new_login():
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

@db_session
def test_new_pass_second_time():
    recovery = db.RecoveryCode.get(username="tiffbri")
    code = recovery.code
    payload = json.dumps({
        "username": "tiffbri",
        "code": code,
        "password": "Tiffany123"
    })
    response = client.put("/pass-change",
                            data=payload)
    assert response.status_code == 403