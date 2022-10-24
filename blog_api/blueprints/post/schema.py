from datetime import datetime
from typing import Optional
from pydantic import BaseModel, constr


class RequestFormCreatePostModel(BaseModel):
    title: str
    body: str


class ResponseCreatePostModel(BaseModel):
    message: str


class RequestFormUpdatePostModel(BaseModel):
    title: Optional[str]
    body: Optional[str]


class ResponsePostModel(BaseModel):
    id: int
    title: constr(max_length=255)
    body: str
    created_time: datetime
    user_id: int

    class Config:
        orm_mode = True
