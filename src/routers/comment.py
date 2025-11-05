import uuid
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from ..models.comment import CommentIn, CommentOut, UserPostWithComment
from ..database import post_table, comment_table, database
import logging


router = APIRouter()

logger = logging.getLogger(__name__)

async def find_post(post_id: UUID4):
    logger.info(f"Finding post: {post_id}")
    query = post_table.select().where(post_table.c.id == str(post_id))
    logger.debug(query)
    return await database.fetch_one(query)


@router.get("/comment/{post_id}", response_model=list[CommentOut])
async def get_comments_on_post(post_id: UUID4):
    query = comment_table.select().where(comment_table.c.post_id == str(post_id))
    return await database.fetch_all(query)


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: UUID4):
    post = await find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post found!")

    return {"post": post, "comments": await get_comments_on_post(post_id)}


@router.post("/comment", response_model=CommentOut, status_code=201)
async def create_comment(comment: CommentIn):
    post = await find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post does not exists.")

    data = comment.model_dump()
    new_comment = {**data, "id": str(uuid.uuid4())}
    query = comment_table.insert().values(new_comment)
    record_id = await database.execute(query)
    return {**new_comment, "id": str(record_id)}
