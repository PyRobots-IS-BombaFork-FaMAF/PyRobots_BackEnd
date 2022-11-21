from types import ModuleType
from fastapi import *
from pony.orm import *
from typing import Optional
from app.core.models.base import db
from app.core.models.robot_models import *
from app.core.models.user_models import *
from app.core.handlers.robot_handlers import *
from app.core.handlers.auth_handlers import *
from app.core.game.robot import Robot as RobotClass
from fastapi.responses import JSONResponse
import uuid
import base64

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
            code_name = CODEDIR + code.filename

            with open(f"{code_name}", "wb") as f:
                f.write("from app.core.game.robot import Robot\n".encode('utf-8') + contents)

            validate_robot_code(
                code_name.replace('/', '.')[:-3],
                get_original_filename(current_user["username"], robot.name, code.filename)[:-3]
            )
        except Exception as error:
            if type(error) == HTTPException:
                raise HTTPException(error.status_code, error.detail)
            else:
                raise HTTPException(400, "Error leyendo el archivo.")
        finally:
            code.file.close()

        robot = db.Robot(
            name=robot.name.lower(),
            avatar=avatar_name,
            code=code_name,
            user=current_user["username"]
        )

        db.RobotStatistics(
            robot_id = get_robot_id(current_user["username"], robot.name)
        )

        msg = "¡Se creo el robot " + robot.name + " con éxito!"

    else:
        if is_robot_created(current_user, robot):
            raise HTTPException(
                409, detail="Ya existe un robot con ese nombre"
            )

    return {msg}

@router.get("/robot/list", status_code=200, tags=["robots"])
@db_session
def list_robots(
    current_user: User = Depends(get_current_active_user)
):
    """
    returns a list of all created robots that the user has
    """
    uname = current_user["username"]
    robots = db.select("select * from Robot where user = $uname or user is null")[:]
    listRobots = dict()
    listRobotsUser = []
    for robot in robots:
        listRobots = {
                'id': robot.id,
                'name': robot.name,
                'avatar': robot.avatar
            }
        listRobotsUser.append(listRobots)

    return JSONResponse(listRobotsUser)

@router.get("/robot/statistics", status_code=200, tags=["robots"])
@db_session
def statistics_robots(
    current_user: User = Depends(get_current_active_user)
):
    """
    returns a list of all created robots that the user has
    """
    uname = current_user["username"]
    robots = db.select("select id, name, avatar from Robot where user = $uname")[:]

    listRobots = dict()
    listRobotsUser = []
    for robot in robots:
        robotStatistics = db.select("select * from RobotStatistics where robot_id = $robot.id")[:]
        for robotStats in robotStatistics:
            with open(robot.avatar, 'rb') as f:
                avatar_img = base64.b64encode(f.read())
                f.close()
            listRobots = {
                'robot_id': robotStats.robot_id,
                'robot_name': robot.name,
                'gamesPlayed': robotStats.gamesPlayed,
                'wins': robotStats.wins,
                'tied': robotStats.tied,
                'losses': robotStats.losses,
                'avatar_name': robot.avatar.rsplit('/', 1)[1],
                'avatar_img': str(avatar_img)
            }
            listRobotsUser.append(listRobots)

    return JSONResponse(listRobotsUser)


def validate_robot_code(pathToCode: str, robotClassName: str):
    """
    Validates the code of the robot
    `pathToCode` has to be in python format (e.g. 'app.robot_code.robot1')

    Trows an exception if the code is invalid
    """
    robotModule: ModuleType = __import__(pathToCode, fromlist=[robotClassName])
    try:
        robotClass: type = getattr(robotModule, robotClassName)
    except:
        raise HTTPException(400, detail= "El nombre del archivo debe ser igual al nombre de la clase.")
    if not issubclass(robotClass, RobotClass):
        raise HTTPException(400, detail="La clase del robot debe heredar de Robot.")
