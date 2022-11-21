from app.core.models.base import db
from datetime import datetime
from pony.orm import db_session
import random
import string
import yagmail

class RecoveryMail:

    def __init__(self):
        self.recovery_code = self.get_random_string(10)

    def get_random_string(self, length):
        result_str = ''.join(random.choice(string.ascii_letters)
                             for i in range(length))
        return result_str

    @db_session
    def send_mail(self, to, username):
        from_user = "pyrobotsfamaf@gmail.com"
        password = "rkioqsrmpflkkvgg"

        body = "Hola " + username + ", haz solicitado una nueva contraseña para tu cuenta. \n"
        body += "Para completar el proceso utiliza el siguiente código: \n"
        body += self.recovery_code
        body += "\n El código expirará dentro de 24 horas, luego de este tiempo deberás generar una nueva solicitud."
        body += "\n Si no solicitaste el cambio puedes ignorar este mensaje."

        yag = yagmail.SMTP(from_user, password)
        yag.send(to, "PyRobots password recovery", body)

        try:
          recovery = db.RecoveryCode.get(username=username)
        except:
          pass
        if recovery == None:
          db.RecoveryCode(
            username=username,
            code=self.recovery_code,
            date_issue=datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f"))
        else:
          recovery.code = self.recovery_code
          recovery.date_issue = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
          recovery.active = 1
