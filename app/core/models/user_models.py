from pydantic import BaseModel, Field, validator
from typing import Optional
from pydantic.networks import EmailStr
from fastapi import *


class UserIn(BaseModel):
    '''
    BaseModel for the user, determines the data collected 
    to access the user endpoints
    '''
    username: str = Field(..., min_length=6, max_length=12)
    email: EmailStr
    password: str = Field(..., min_length=8, max_length=16,
                          regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")

    @validator('*', pre=True)
    def remove_blank_strings(cls, v):
        """Removes whitespace characters and return None if empty"""
        if isinstance(v, str):
            v = v.strip()
        if v == "":
            return None
        return v

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
                          regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")
    avatar: Optional[str] = None
    validated: Optional[bool] = False


class Token(BaseModel):
    access_token: str
    token_type: str


class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=8,
                          regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")
    new_password: str = Field(..., min_length=8,
                          regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")

class NewPass(BaseModel):
    '''
    BaseModel for the data neccesary
    to generate a new password
    '''
    username: str
    code: str
    password: str = Field(..., min_length=8,
                          regex=r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)[a-zA-Z\d\w\W]{8,}$")
