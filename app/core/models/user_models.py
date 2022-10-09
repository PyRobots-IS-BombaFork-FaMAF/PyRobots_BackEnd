from tokenize import String
from pydantic import BaseModel, Field
from typing import Optional
from pydantic.networks import EmailStr

class User(BaseModel):
    '''
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    '''
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8,
                          regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{8,}$")
    # avatar ?
    email_confirmed: Optional[bool] = False