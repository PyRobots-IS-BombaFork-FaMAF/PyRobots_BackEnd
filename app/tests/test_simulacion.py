from calendar import c
from datetime import datetime
from fastapi.testclient import TestClient
from app.tests.test_main import app_test
from app.core.models.base import User, Validation_data, db, Robot
from pony.orm import *
from urllib.parse import quote
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
                "id": 1
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
    assert response.status_code == 201