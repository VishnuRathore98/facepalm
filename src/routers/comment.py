import uuid
from fastapi import APIRouter, HTTPException
from pydantic import UUID4
from src.models.comment import CommentIn, CommentOut, UserPostWithComment
from src.routers.post import post_table


router = APIRouter()
comment_table = {}


def find_post(post_id: UUID4):
    return post_table.get(post_id)


@router.get("/comment/{post_id}", response_model=list[CommentOut])
async def get_comments_on_post(post_id: UUID4):
    return [
        comment for comment in comment_table.values()
        if comment['post_id'] == post_id
    ]


@router.get("/post/{post_id}", response_model=UserPostWithComment)
async def get_post_with_comments(post_id: UUID4):
    post = find_post(post_id)
    if not post:
        raise HTTPException(status_code=404, detail="No Post found!")

    return {"post": post, "comments": await get_comments_on_post(post_id)}


@router.post("/comment", response_model=CommentOut, status_code=201)
def create_comment(comment: CommentIn):
    post = find_post(comment.post_id)
    if not post:
        raise HTTPException(status_code=404, detail="Post does not exists.")

    data = comment.model_dump()
    id = len(comment_table)
    new_comment = {**data, "id": uuid.uuid4()}
    comment_table[id] = new_comment

    return new_comment
