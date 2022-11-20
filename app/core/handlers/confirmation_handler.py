from app.core.models.base import db
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pony.orm import db_session, commit
from urllib.parse import quote
import random
import string
import smtplib
import yagmail
from datetime import date

@db_session
def send_confirmation_mail(to, username):
    from_user = "pyrobotsfamaf@gmail.com"
    password = "rkioqsrmpflkkvgg"

    body = "Hola " + username + ", registramos un cambio de contraseña el día "
    body += date.today().strftime("%d/%m/%Y") + ".\n Ya puedes acceder a tu cuenta con tu nueva contraseña."

    yag = yagmail.SMTP(from_user, password)
    yag.send(to, "PyRobots cambio de contraseña", body)

