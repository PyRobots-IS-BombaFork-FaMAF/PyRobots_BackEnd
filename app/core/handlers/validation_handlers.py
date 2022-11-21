from app.core.models.base import db
from pony.orm import db_session
from urllib.parse import quote
import random
import string
import yagmail


class ValidationMail:

    def __init__(self):
        self.verification_code = self.get_random_string(10)

    def get_random_string(self, length):
        result_str = ''.join(random.choice(string.ascii_letters)
                             for i in range(length))
        return result_str

    @db_session
    def send_mail(self, to, username):
        from_user = "pyrobotsfamaf@gmail.com"
        password = "rkioqsrmpflkkvgg"

        body = "Hola " + username + " ¡Gracias por registrar una cuenta en PyRobots! \n"
        body += "Antes de comenzar, solo necesitamos confirmar que eres tú."
        body += " Haz clic a continuación para verificar tu dirección de correo electrónico \n"
        body += "http://127.0.0.1:3000/validate?email=" + \
            quote(to) + "&code=" + self.verification_code

        yag = yagmail.SMTP(from_user, password)
        yag.send(to, "PyRobots account verification", body)

        db.Validation_data(email=to, code=self.verification_code)
