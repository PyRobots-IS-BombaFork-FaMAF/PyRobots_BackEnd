from tokenize import String
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional
from pydantic.networks import EmailStr
from fastapi import *

class UserIn(BaseModel):
    '''
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    '''
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8,
                          regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")

    @classmethod
    def as_form(cls, username: str = Form(...), email: EmailStr = Form(...), password: str = Form(...)) -> 'UserIn':
        return cls(username=username, email=email, password=password)

class User(BaseModel):
    '''
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    '''
    username: str
    email: EmailStr
    password: str = Field(..., min_length=8,
                          regex="^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")
    avatar: Optional[str] = None
    email_confirmed: Optional[bool] = False