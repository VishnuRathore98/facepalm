from pydantic import UUID4, BaseModel
from .post import UserPostIn


class CommentIn(BaseModel):
    body: str
    post_id: UUID4


class CommentOut(CommentIn):
    id: int


class UserPostWithComment(BaseModel):
    post: UserPostIn
    comments: list[CommentIn]
