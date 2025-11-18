import uuid
from fastapi import APIRouter, Depends
from models.post import UserPostIn, UserPostOut
from database import post_table, database
import logging
from security import get_current_user


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/posts",
    response_model=UserPostOut,
    status_code=201,
    dependencies=[Depends(get_current_user)],
)
async def create_post(post: UserPostIn):
    data = post.model_dump()
    new_post = {**data, "id": str(uuid.uuid4())}
    query = post_table.insert().values(new_post)
    record_id = await database.execute(query)
    return {**new_post, "record_id": record_id}


@router.get(
    "/posts",
    response_model=list[UserPostOut],
    dependencies=[Depends(get_current_user)],
)
async def get_posts():
    logger.info("Getting Posts")
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)
