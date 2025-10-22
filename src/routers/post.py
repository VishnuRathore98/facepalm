import uuid
from fastapi import APIRouter
from src.models.post import UserPostIn, UserPostOut

router = APIRouter()

post_table={}

@router.post("/posts", response_model=UserPostOut)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    new_post = {**data, "id": uuid.uuid4()}
    id=len(post_table)
    post_table[id] = new_post
    return new_post

@router.get("/posts", response_model=list[UserPostOut])
async def get_posts():
    return list(post_table.values())
