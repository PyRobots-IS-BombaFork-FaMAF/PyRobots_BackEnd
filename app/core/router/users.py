from fastapi import APIRouter, Depends, HTTPException, status, BackgroundTasks, responses, Response
from pony.orm import *

from app.core.models.base import db 
from app.core.models.user_models import User
from app.core.handlers.password_handlers import *
from app.core.handlers.validation_handlers import *
from app.core.handlers.userdb_handlers import *

tags_metadata = [
    {
        "name": "users",
        "description": "Operations with users. The **login** logic is also here.",
    }
]
    
router = APIRouter()

@router.post("/users/register", tags=["Users"], status_code=201)
@db_session
def register(user: User, background_t: BackgroundTasks):
    if not(is_username_registered(user) or is_email_registered(user)):
        db.User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password)
        )
        validator = ValidationMail()
        background_t.add_task(validator.send_mail, user.email, user.username)
        msg = user.username + ", se ha enviado un mail de verifiación a " + user.email 
    
    else:
        msg = ""
        if is_username_registered(user):
            msg += "Usuario ya existente"
            raise HTTPException(
                status_code = 409, detail = "Usuario ya existente"
            )
        elif is_email_registered(user):
            msg+= "El e-mail ya se encuentra registrado"
            raise HTTPException(
                status_code = 409, detail = "El e-mail ya se encuentra registrado"
            )
    
    return {msg}