from fastapi.testclient import TestClient
from app.tests.test_main import app_test

client = TestClient(app_test)

def test_register_valid_user_with_avatar():
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"avatar" : ("image_file", avatar_img, "image/jpeg")}
    response = client.post("users/register",
                            data={
                                "username": "tiffbr",
                                "email": "tiffanybricett1r996@gmail.com",
                                "password": "Tiffanyb19!"
                            },
                            files = avatar
                            )
    assert response.status_code == 201

def test_register_valid_user_without_avatar():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "Tiffanyb19!"
                            }
                            )
    assert response.status_code == 201

def test_register_valid_user_without_avatar():
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"avatar" : ("image_file", avatar_img, "image/jpeg")}
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "Tiffanyb19!"
                            }
                            )
    print(response.json())
    assert response.status_code == 201

def test_post_invalid_email_user_without_avatar():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996gmail.com",
                                "password": "Tiffanyb19!"
                            }
                            )
    assert response.status_code == 422

def test_post_invalid_email_user_with_avatar():
    with open('app/avatars/default.jpg', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"avatar" : ("image_file", avatar_img, "image/jpeg")}
    response = client.post("users/register",
                            data={
                                "username": "tiffbr",
                                "email": "tiffanybricett1r996gmail.com",
                                "password": "Tiffanyb19!"
                            },
                            files = avatar
                            )
    assert response.status_code == 422

def test_post_invalid_password_user():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "Tiffanybricett" #no numbers
                            }
                            )
    assert response.status_code == 422

def test_post_invalid_password_user2():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "tiffanybricett1" #no uppercase
                            }
                            )
    assert response.status_code == 422

def test_post_invalid_password_user3():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "TIFFANYB1928" #no lowercase
                            }
                            )
    assert response.status_code == 422

def test_post_invalid_password_user4():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "tiffanybricett1996@gmail.com",
                                "password": "Tb19" #length < 8
                            }
                            )
    assert response.status_code == 422

def test_register_invalid_file_avatar():
    with open('app/avatars/Glosario.docx', 'rb') as f:
        avatar_img = f.read()
        f.close()
    avatar = {"avatar" : ("image_file", avatar_img, "image/jpeg")}
    response = client.post("users/register",
                            data={
                                "username": "tiffbr",
                                "email": "tiffanybricett1r996@gmail.com",
                                "password": "Tiffanyb19!"
                            },
                            files = avatar
                            )
    assert response.status_code == 409

def test_post_invalid_mail_user():
    response = client.post("users/register",
                            data={
                                "username": "tiffbro",
                                "email": "@gmail.com",
                                "password": "Tb19jdjdj82" #length < 8
                            }
                            )
    assert response.status_code == 422