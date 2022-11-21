from pony.orm import db_session
from app.core.models.robot_models import RobotIn
from app.core.models.user_models import User
from app.core.models.base import db


@db_session
def is_robot_created(u: User, r: RobotIn):
    uname = u["username"].lower()
    rname = r.name.lower()
    return db.exists("select * from Robot where name = $rname and user = $uname")

db_session
def get_robot_id(u: str, r: str):
    robot = None
    try:
        robot = db.get("select * from Robot where name = $r and user = $u")
    except:
        pass
    return robot.id

def generate_file_name(filename: str, u: User, r: RobotIn):
    uname = u["username"]
    return f"{uname.lower() + r.name.lower() + filename}"


def get_original_filename(u: User, r: str, filename: str):
    if isinstance(u, User): 
        uname = u["username"]
    else:
        uname = u
    return filename[len(uname) + len(r):]
