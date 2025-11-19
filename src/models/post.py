from pydantic import UUID4, BaseModel


class UserPostIn(BaseModel):
    body: str


class UserPostOut(UserPostIn):
    id: UUID4
    user_id: str
