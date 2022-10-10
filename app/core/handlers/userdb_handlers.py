from pony.orm import db_session, select
from app.core.models.user_models import UserIn
from app.core.models.base import db  

@db_session
def is_username_registered(u: UserIn):
    uname = u.username
    return db.exists("select * from User where username = $uname")

@db_session
def is_email_registered(u: UserIn):
    uemail = u.email
    return db.exists("select * from User where email = $uemail")