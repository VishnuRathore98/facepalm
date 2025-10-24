from pydantic import BaseModel
from .post import UserPostIn


class CommentIn(BaseModel):
    body: str
    post_id: int


class CommentOut(CommentIn):
    id: int


class UserPostWithComment(BaseModel):
    post: UserPostIn
    comments: list[CommentIn]
