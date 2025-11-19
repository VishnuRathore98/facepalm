from pydantic import BaseModel


class User(BaseModel):
    id: str | None = None
    email: str


class UserIn(User):
    password: str
