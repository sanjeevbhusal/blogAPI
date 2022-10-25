from pydantic import BaseModel


class CommentResponse(BaseModel):
    id: int
    message: str
    post_id: int
    author_id: int

    class Config:
        orm_mode = True


class CommentCreate(BaseModel):
    message: str
    post_id: str
