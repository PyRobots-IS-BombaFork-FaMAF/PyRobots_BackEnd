from pony.orm import db_session
import yagmail
from datetime import date

@db_session
def send_confirmation_mail(to, username):
    from_user = "pyrobotsfamaf@gmail.com"
    password = "rkioqsrmpflkkvgg"

    body = "Hola " + username + ", hemos registrado un cambio de contraseña el día "
    body += date.today().strftime("%d/%m/%Y") + ".\n Ya puedes acceder a tu cuenta con la nueva contraseña."

    yag = yagmail.SMTP(from_user, password)
    yag.send(to, "PyRobots cambio de contraseña", body)