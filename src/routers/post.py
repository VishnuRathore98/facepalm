from typing import Annotated
import uuid
from fastapi import APIRouter, Depends
from models.post import UserPostIn, UserPostOut
from database import post_table, database
import logging
from security import get_current_user
from models.users import User


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post(
    "/posts",
    response_model=UserPostOut,
    status_code=201,
)
async def create_post(
    post: UserPostIn, current_user: Annotated[User, Depends(get_current_user)]
):
    data = post.model_dump()
    print(">>> Current user: ", current_user)
    new_post = {**data, "id": str(uuid.uuid4()), "user_id": current_user.id}
    query = post_table.insert().values(new_post)
    print("query: ", query)
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
