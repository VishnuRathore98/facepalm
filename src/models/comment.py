from pydantic import BaseModel
from .post import UserPostOut


class CommentIn(BaseModel):
    body: str
    post_id: str


class CommentOut(CommentIn):
    id: str
    user_id: str


class UserPostWithComment(BaseModel):
    post: UserPostOut
    comments: list[CommentOut]
