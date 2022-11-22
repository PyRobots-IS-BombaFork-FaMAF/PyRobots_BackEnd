from datetime import datetime, timedelta
from fastapi import *
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordRequestForm
from pony.orm import *
from typing import Optional
from app.core.models.base import db
from app.core.models.user_models import UserIn, User, Token, PasswordChange, NewPass
from app.core.handlers.auth_handlers import *
from app.core.handlers.password_handlers import *
from app.core.handlers.recovery_handler import *
from app.core.handlers.validation_handlers import *
from app.core.handlers.userdb_handlers import *
from app.core.handlers.confirmation_handler import *
from urllib.parse import unquote
import uuid
import os
import base64

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
@db_session
def validate_user(email: str, code: str):
    """
    validation endpoint to allow users to validate their account by
    clicking on the link they receive by e-mail, that way they can 
    log in and start playing
    """
    user = db.User.get(email=email)
    if user != None and user.validated:
        msg = "Ya tu cuenta se encuentra validada"
    elif user != None and not user.validated:
        try:
            email = unquote(email)
            data = db.get(
                "select email,code from Validation_data where email=$email")
        except:
            raise HTTPException(status_code=404, detail="Email no encontrado")

        if data[1] != code:
            raise HTTPException(
                status_code=409, detail="Código de validación inválido")
        user.validated = True
        msg = "¡Hemos validado tu cuenta!"
    else:
        raise HTTPException(status_code=404, detail="Usuario inexistente")
    return msg


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
    if not user["validated"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario no validado",
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

@router.put("/user/avatar", tags=["Users"], status_code=200)
@db_session
def change_avatar(
    current_user: User = Depends(get_current_active_user),
    new_avatar: Optional[UploadFile] = File(None)):

    """
    Endpoint to change the avatar
    """

    uname = current_user["username"]

    if new_avatar != None and new_avatar.filename != "":
        if new_avatar.content_type not in ['image/jpeg', 'image/png', 'image/tiff', 'image/jpg']:
            raise HTTPException(
                409, detail="Tipo de archivo inválido")
        else:
            new_avatar.filename = f"{uname + str(uuid.uuid4())}.jpg"
            try:
                new_avatar.file.seek(0)
                contents = new_avatar.file.read()  # Important to wait
                avatar_name = IMAGEDIR + new_avatar.filename

                with open(f"{avatar_name}", "wb") as f:
                    f.write(contents)
            except:
                raise HTTPException(
                    400, detail="Error leyendo imagen")
            finally:
                new_avatar.file.close()
    else:
        raise HTTPException(status_code=403, detail= "El archivo esta vacio")

    user = db.User[uname]
    try:
        user.avatar = avatar_name
        msg = "Se ha cambiado el avatar exitosamente"
    except: 
        raise HTTPException(status_code=400, detail= "Error cambiando el avatar")

    return msg


@router.put("/user/password", tags=["Users"], status_code=200)
@db_session
def change_password(
    passwords: PasswordChange,
    current_user: User = Depends(get_current_active_user),
    background_t: BackgroundTasks = BackgroundTasks()):
    
    uname = current_user["username"]
    user = db.User[uname]

    if verify_password(user.password, passwords.old_password):
        try:
            user.password = hash_password(passwords.new_password)
            msg = "Se cambio la contraseña con éxito"
            background_t.add_task(send_confirmation_mail, user.email, uname)

        except:
            raise HTTPException(status_code=400, detail= "Error cambiando el password")

    else: 
        raise HTTPException(status_code=401, detail="Password incorrecto")

    return msg

@router.get("/user/info", status_code=200, tags=["Users"])
@db_session
def user_info(
    current_user: User = Depends(get_current_user)):
    """
        Returns user information
    """
    uname = current_user["username"]
    uavatar = current_user["avatar"]
    uemail = current_user["email"]

    with open(uavatar, 'rb') as f:
        avatar_img = base64.b64encode(f.read())
        f.close()

    current_user_info = {
        'name': uname,
        'email': uemail,
        'avatar_name': uavatar.rsplit('/', 1)[1], 
        'avatar_img': str(avatar_img)
    }
    
    if os.path.exists(uavatar):
       return JSONResponse(current_user_info)
    else: 
       raise HTTPException(status_code=403, detail= "No se encontró el archivo")


@router.get("/pass-recovery")
@db_session
def send_code(username: str, background_t: BackgroundTasks = BackgroundTasks()):
    """
    Endpoint to request a password recovery, 
    the user recieves a code by email that can
    be used to generate a new password
    """
    user = db.User.get(username = username)
    if user != None:
        recovery = RecoveryMail()
        background_t.add_task(recovery.send_mail, user.email, user.username)
    
    msg = "¡Hemos enviado un código de recuperación a tu email!"
    return msg

@router.put("/pass-change")
@db_session
def new_password(newpass: NewPass):
    try:
        user = db.User.get(username = newpass.username)
    except:
        raise HTTPException(
                status_code=403, detail="Usuario inexistente")
    if user == None:
        raise HTTPException(
                status_code=403, detail="Usuario inexistente")
    else:
        try:
            recovery = db.RecoveryCode.get(username=newpass.username)
        except:
            raise HTTPException(
                    status_code=403, detail="Código de recuperación inválido")
        if recovery != None:
            time_diff = (datetime.now() - recovery.date_issue).seconds
            print(time_diff)
            # Checking if the code hasn't been issued for over a day
            if newpass.code == recovery.code and time_diff < 86400 and recovery.active:
                user.password = hash_password(newpass.password)
                recovery.active = 0
                msg = "¡La contraseña se ha cambiado exitosamente!"
            else:
                raise HTTPException(
                    status_code=403, detail="Código de recuperación inválido")
        else:
            raise HTTPException(
                status_code=403, detail="Código de recuperación inválido")

    return msg

