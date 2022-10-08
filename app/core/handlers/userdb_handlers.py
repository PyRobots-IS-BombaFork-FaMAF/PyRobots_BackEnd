from pony.orm import db_session, select
from app.core.models.user_models import User
from app.core.models.base import db  

@db_session
def is_username_registered(u: User):
    uname = u.username
    return db.exists("select * from User where username = $uname")

@db_session
def is_email_registered(u: User):
    uemail = u.email
    return db.exists("select * from User where email = $uemail")