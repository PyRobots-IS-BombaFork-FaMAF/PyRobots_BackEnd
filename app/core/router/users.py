from datetime import datetime, timedelta
from fastapi import *
from fastapi.responses import JSONResponse, HTMLResponse, FileResponse
from fastapi.security import OAuth2PasswordRequestForm
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db
from app.core.models.user_models import UserIn, User, Token
from app.core.handlers.auth_handlers import *
from app.core.handlers.password_handlers import *
from app.core.handlers.validation_handlers import *
from app.core.handlers.userdb_handlers import *
from urllib.parse import unquote
import uuid
import os

IMAGEDIR = "app/avatars/"

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    }
]

router = APIRouter()


@router.post("/users/register", tags=["Users"], status_code=201)
@db_session
def register(
        user: UserIn = Depends(UserIn.as_form),
        avatar: Optional[UploadFile] = File(None),
        background_t: BackgroundTasks = BackgroundTasks()):
    if not(is_username_registered(user) or is_email_registered(user)):
        if avatar != None and avatar.filename != "":
            if avatar.content_type not in ['image/jpeg', 'image/png', 'image/tiff', 'image/jpg']:
                raise HTTPException(
                    409, detail="Tipo de archivo inválido")
            else:
                avatar.filename = f"{user.username + str(uuid.uuid4())}.jpg"
                try:
                    avatar.file.seek(0)
                    contents = avatar.file.read()  # Important to wait
                    avatar_name = IMAGEDIR + avatar.filename

                    with open(f"{avatar_name}", "wb") as f:
                        f.write(contents)
                except:
                    raise HTTPException(
                        400, detail="Error leyendo imagen")
                finally:
                    avatar.file.close()

        else:
            avatar_name = IMAGEDIR + "default.jpg"

        db.User(
            username=user.username.lower(),
            email=user.email.lower(),
            password=hash_password(user.password),
            avatar=avatar_name
        )

        validator = ValidationMail()
        msg = user.username + ", se ha enviado un mail de verificación a " + user.email
        background_t.add_task(validator.send_mail, user.email, user.username)

    else:
        if is_username_registered(user):
            raise HTTPException(
                409, detail="Usuario ya existente"
            )
        elif is_email_registered(user):
            raise HTTPException(
                409, detail="El e-mail ya se encuentra registrado"
            )

    return {msg}


@router.get("/validate", tags=["Users"], status_code=200)
async def validate_user(email: str, code: str):
    """
    validation endpoint to allow users to validate their account by
    clicking on the link they receive by e-mail, that way they can 
    log in and start playing
    """
    with db_session:
        try:
            email = unquote(email)
            data = db.get(
                "select email,code from Validation_data where email=$email")
        except:
            raise HTTPException(status_code=404, detail="Email no encontrado")

        if data[1] != code:
            raise HTTPException(
                status_code=409, detail="Código de validación invalido")
        print()
        user = db.User.get(email=email)
        user.validated = True
        db.commit()
    html = """
<!DOCTYPE html>
<html>
    <head>
        <title>PyRobots</title>
    </head>
    <body style="background-color:white; text-align: center;">
        <h1 style="text-align: center; padding-top: 60px;font-family:verdana" >¡E-mail validado!</h1>
        <h5 style="text-align: center;font-family:verdana" >
            ¡Ya puedes empezar a jugar!
        </h5>
        <div>
            <img src="https://img.freepik.com/vector-gratis/juguete-robot-vintage-sobre-fondo-blanco_1308-77501.jpg"; style="width: 300px;height: 400px;">
            </img>
        </div>
    </body>
</html>
"""
    return HTMLResponse(html)


@router.post("/token", tags=["Login"], response_model=Token, status_code=200)
async def login_for_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    LogIn endpoint, first, authenticates the user checking that the
    username and the password submitted by the user are correct.
    Then it creates a valid token for the user.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña o usuario incorrecto",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"username": user["username"].lower()},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.put("/users/refresh", tags=["Login"], response_model=Token, status_code=201)
async def refresh_token(username: str = Depends(valid_credentials)):
    """
    Endpoint that creates a new web token.
    Need to be logged in to use.
    """
    if not username:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Contraseña incorrecta",
            headers={"WWW-Authenticate": "Bearer"},
        )

    try:
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = create_access_token(
            data={"username": username},
            expires_delta=access_token_expires,
        )
        return {"access_token": access_token, "token_type": "bearer"}
    except:
        raise HTTPException(
            status_code=405,
            detail="Algo salió mal"
        )


@router.get("/users/me/", response_model=User)
async def read_users_me(current_user: User = Depends(get_current_active_user)):
    return current_user


@router.get("/logout")
async def logout(request: Request, current_user: User = Depends(get_current_active_user)):
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect password",
        headers={"WWW-Authenticate": "Bearer"},
    )

@router.get("/user/info", status_code=200, tags=["Users"])
@db_session
def user_info(
    current_user: User = Depends(get_current_active_user)):
    """
        Returns user information
    """
    uname = current_user["username"]
    uavatar = current_user["avatar"]
    uemail = current_user["email"]

    current_user_info = {
        'name': uname,
        'email': uemail
    }
    
    if os.path.exists(uavatar):
       return FileResponse(uavatar, headers = current_user_info, media_type="image/jpeg")
    else: 
       raise HTTPException(status_code=403, detail= "No se encontro el archivo")






