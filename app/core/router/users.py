from tokenize import String
from fastapi import *
from fastapi.responses import JSONResponse
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db 
from app.core.models.user_models import UserIn, User
from app.core.handlers.password_handlers import *
from app.core.handlers.validation_handlers import *
from app.core.handlers.userdb_handlers import *
import uuid

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
    avatar: Optional[UploadFile] = File(None)):
    if not(is_username_registered(user) or is_email_registered(user)):
        if avatar != None and avatar.filename != "":
            if avatar.content_type not in ['image/jpeg', 'image/png', 'image/tiff']:
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
            avatar_name = "default.jpg"

        db.User(
            username = user.username,
            email = user.email,
            password = hash_password(user.password),
            avatar = avatar_name
        )

        validator = ValidationMail()
        msg = user.username + ", se ha enviado un mail de verificación a " + user.email 
        background_t = BackgroundTasks()
        background_t.add_task(validator.send_mail, user.email, user.username)
        
    else:
        if is_username_registered(user):
            raise HTTPException(
                409, detail = "Usuario ya existente"
            )
        elif is_email_registered(user):
            raise HTTPException(
                409, detail = "El e-mail ya se encuentra registrado"
            )
    
    return {msg}