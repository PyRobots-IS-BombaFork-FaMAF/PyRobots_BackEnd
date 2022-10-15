from fastapi import *
from pony.orm import *
from typing import Union, Optional
from app.core.models.base import db
from app.core.models.robot_models import *
from app.core.models.user_models import *
from app.core.handlers.robot_handlers import *
from app.core.handlers.auth_handlers import *
import uuid

IMAGEDIR = "app/robot_avatars/"
CODEDIR = "app/robot_code/"

router = APIRouter()


@router.post("/robots/create", tags=["robots"], status_code=201)
@db_session
def register(
        current_user: User = Depends(get_current_active_user),
        robot: RobotIn = Depends(RobotIn.form),
        avatar: Optional[UploadFile] = File(None),
        code: UploadFile = File(...)):
    if not(is_robot_created(current_user, robot)):
        if code == None or code.filename == "":
            raise HTTPException(
                400, detail="El archivo con el código es obligatorio"
            )
        elif (code.content_type not in
              ["text/x-python", "application/x-python-code",
                  "application/octet-stream"]
                or '.py' not in code.filename):
            raise HTTPException(
                415, detail="Tipo de archivo inválido")
        else:
            code.filename = generate_file_name(
                code.filename, current_user, robot)

        if avatar != None and avatar.filename != "":
            if (avatar.content_type not in
                    ['image/jpeg', 'image/png', 'image/tiff', 'image/jpg']):
                raise HTTPException(
                    409, detail="Tipo de archivo inválido")
            else:
                uname = current_user["username"]
                avatar.filename = f"{uname + robot.name + str(uuid.uuid4())}.jpg"
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

        try:
            code.file.seek(0)
            contents = code.file.read()  # Important to wait
            print(code.filename)
            code_name = CODEDIR + code.filename

            with open(f"{code_name}", "wb") as f:
                f.write(contents)
        except:
            raise HTTPException(
                400, detail="Error leyendo archivo")
        finally:
            code.file.close()

        db.Robot(
            name=robot.name,
            avatar=avatar_name,
            code=code_name,
            user=current_user["username"]
        )

        msg = "¡Se creo el robot " + robot.name + " con éxito!"

    else:
        if is_robot_created(current_user, robot):
            raise HTTPException(
                409, detail="Ya existe un robot con ese nombre"
            )

    return {msg}
