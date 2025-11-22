import logging
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from security import get_current_user
from models.likes import PostLike, PostLikeIn
from routers.comment import find_post
import database
from database import like_table
from src.models.users import User


router = APIRouter()
logger = logging.getLogger(__file__)


@router.post(path="/like", response_model=PostLike, status_code=201)
async def like_post(
    like: PostLikeIn, current_user: Annotated[User, Depends(get_current_user)]
):
    logger.info("Liking post")
    post = await find_post(like.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="post not found")

    data = {**like.model_dump(), "user_id": current_user.id}
    query = like_table.insert().values(data)

    logger.debug(query)

    last_record_id = await database.execute(query)
    return {**data, "id": last_record_id}
