from fastapi import APIRouter, HTTPException, status
from sqlalchemy.sql.roles import AllowsLambdaRole
from src.models.users import UserIn
from src.security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user,
)
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
    hashed_password = get_password_hash(user.password)

    query = user_table.insert().values(
        email=user.email,
        password=hashed_password,
    )

    logger.debug(query)

    await database.execute(query)
    return {"message": "User created."}


@router.post("/login")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(user.email)
    return {"access_token": access_token, "token_type": "bearer"}
