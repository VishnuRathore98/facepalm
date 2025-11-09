from fastapi import APIRouter, HTTPException, status
from src.models.users import UserIn
from src.security import get_user
import logging
from src.database import user_table, database


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )

    query = user_table.insert().values(
        email=user.email,
        password=user.password,
    )

    logger.debug(query)

    await database.execute(query)
    return {"message": "User created."}
