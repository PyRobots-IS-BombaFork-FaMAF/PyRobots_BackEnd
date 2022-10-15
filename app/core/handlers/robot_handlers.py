from pony.orm import db_session, select
from app.core.models.robot_models import Robot, RobotIn
from app.core.models.user_models import User
from app.core.models.base import db  

@db_session
def is_robot_created(u: User, r: RobotIn):
    uname = u["username"]
    rname = r.name
    return db.exists("select * from Robot where name = $rname and user = $uname")

def generate_file_name(filename: str, u: User, r: RobotIn):
    uname = u["username"]
    return f"{uname + r.name + filename}"


def get_original_filename(u: User, r: Robot, filename: str):
    uname = u["username"]
    return filename[len(uname) + len(r.name):]

