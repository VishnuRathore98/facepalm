from fastapi import APIRouter, HTTPException, status
from models.users import UserIn
from security import (
    authenticate_user,
    create_access_token,
    get_password_hash,
    get_user_by_email,
)
import logging
from database import user_table, database


router = APIRouter()

logger = logging.getLogger(__name__)


@router.post("/register", status_code=201)
async def register(user: UserIn):
    if await get_user_by_email(user.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists",
        )
    hashed_password = get_password_hash(user.password)

    query = user_table.insert().values(
        email=user.email,
        password=hashed_password,
    )

    #    print("query", query)
    print(query.compile(compile_kwargs={"literal_binds": True}))
    logger.debug(query)

    await database.execute(query)
    return {"message": "User created."}


@router.post("/login")
async def login(user: UserIn):
    user = await authenticate_user(user.email, user.password)
    access_token = create_access_token(str(user.id))
    return {"access_token": access_token, "token_type": "bearer"}
