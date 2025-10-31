import uuid
from fastapi import APIRouter
from ..models.post import UserPostIn, UserPostOut
from ..database import post_table, database


router = APIRouter()


@router.post("/posts", response_model=UserPostOut, status_code=201)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    new_post = {**data, "id": str(uuid.uuid4())}
    query = post_table.insert().values(new_post)
    record_id = await database.execute(query)
    return {**new_post, "record_id": record_id}


@router.get("/posts", response_model=list[UserPostOut])
async def get_posts():
    query = post_table.select()
    return await database.fetch_all(query)
