from app.core.models.base import db 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from pony.orm import db_session, commit
import random
import string
import smtplib

class ValidationMail:

    def __init__(self):
        self.verification_code = self.get_random_string(10)
    
    def get_random_string(self, length):
        result_str = ''.join(random.choice(string.ascii_letters) for i in range (length))
        return result_str

    @db_session
    def send_mail(self, to, username):
        from_user = "pyrobotsfamaf@gmail.com"
        password = "zjyqmkqicsazrenx"
        
        msg = MIMEMultipart()
        msg["Subject"] = "PyRobots account verification"
        msg["From"] = from_user 
        msg["To"] = to

        body = "Hola " + username + " ¡Gracias por registrar una cuenta en PyRobots! " 
        body += "Antes de comenzar, solo necesitamos confirmar que eres tú." 
        body += " Haz clic a continuación para verificar tu dirección de correo electrónico \n"
        body += "https://127.0.0.1:8000/validate?email=" + to + "&code=" + self.verification_code

        msg.attach(MIMEText(body, 'plain'))

        text = msg.as_string()

        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login(from_user, password=password)
        s.sendmail(from_user, to, text)
        s.close()

        db.Validation_data(email=to, code=self.verification_code)
         