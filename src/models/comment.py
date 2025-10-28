from pydantic import UUID4, BaseModel
from .post import UserPostIn


class CommentIn(BaseModel):
    body: str
    post_id: str


class CommentOut(CommentIn):
    id: str


class UserPostWithComment(BaseModel):
    post: UserPostIn
    comments: list[CommentIn]
