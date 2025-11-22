from pydantic import BaseModel


class PostLikeIn(BaseModel):
    post_id: str


class PostLike(PostLikeIn):
    id: str
    user_id: str
