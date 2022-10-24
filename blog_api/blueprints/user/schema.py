from typing import Optional

from pydantic import BaseModel


class UserRegisterRequestModel(BaseModel):
    email: str
    password: str
    firstname: str
    middlename: Optional[str]
    lastname: str
    bio: str


class UserRegisterResponseModel(BaseModel):
    message: str


class UserLoginRequestModel(BaseModel):
    email: str
    password: str


class UserLoginResponseModel(BaseModel):
    token: str



