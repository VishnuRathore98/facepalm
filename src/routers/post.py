import uuid
from fastapi import APIRouter
from sqlalchemy.sql.functions import current_user
from ..models.post import UserPostIn, UserPostOut
from ..database import post_table, database
import logging
from security import get_current_user, oauth2_scheme
from models.users import User


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/posts", response_model=UserPostOut, status_code=201)
async def create_post(post: UserPostIn):
    current_user: User = await get_current_user(oauth2_scheme())  # noqa
    data = post.model_dump()
    new_post = {**data, "id": str(uuid.uuid4())}
    query = post_table.insert().values(new_post)
    record_id = await database.execute(query)
    return {**new_post, "record_id": record_id}


@router.get("/posts", response_model=list[UserPostOut])
async def get_posts():
    current_user: User = await get_current_user(oauth2_scheme())  # noqa
    logger.info("Getting Posts")
    query = post_table.select()
    logger.debug(query)
    return await database.fetch_all(query)
