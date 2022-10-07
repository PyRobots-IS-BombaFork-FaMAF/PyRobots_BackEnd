from pony.orm import *
from datetime import date
from passlib.context import CryptContext
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

db = Database()

def define_database_and_entities(**db_params):
    global db

    class User(db.Entity):
        username = PrimaryKey(str)
        email = Required(str, unique=True)
        password = Required(str, unique=False)
        validated = Required(bool, unique=False, default=0)

        @staticmethod
        def hash_password(plain_password: str) -> str:
            return pwd_context.hash(plain_password)

        def verify_password(self, plain_password: str) -> bool:
            return pwd_context.verify(plain_password, self.hashed_password)

    db.bind(**db_params)
    db.generate_mapping(create_tables=True)

    pass
