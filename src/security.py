import logging
from passlib.context import CryptContext
from argon2 import PasswordHasher
from database import database, user_table
import datetime
from jose import jwt, JWTError, ExpiredSignatureError
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer


logger = logging.getLogger(__name__)


pwd_context = CryptContext(schemes=["bcrypt"])
ph = PasswordHasher()
ALGORITHM = "HS256"
SECRET = "sldkfjwer23424ro2"
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


credentials_exception = HTTPException(
    status_code=status.HTTP_401_UNAUTHORIZED,
    detail="User not authorized",
    headers={"WWW-Authenticate": "Bearer"},
)


def access_token_exp_min() -> int:
    return 30


def create_access_token(email: str):
    logger.debug("Creating access token", extra={"email": email})
    expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(
        minutes=access_token_exp_min()
    )
    jwd_data = {"sub": email, "exp": expire}
    encoded_jwt = jwt.encode(jwd_data, key=SECRET, algorithm=ALGORITHM)
    return encoded_jwt


def get_password_hash(password: str) -> str:
    print("DEBUG → password repr:", repr(password))
    print("DEBUG → char length:", len(password))
    print("DEBUG → byte length:", len(password.encode()))
    print(f"User password: {password}")
    # return pwd_context.hash(password[:72])
    return ph.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return ph.verify(hashed_password, plain_password)


async def get_user(email: str):
    logger.debug("Fetching user from database", extra={"email": email})
    query = user_table.select().where(user_table.c.email == email)
    result = await database.fetch_one(query)
    if result:
        return result


async def authenticate_user(email: str, password: str):
    logger.debug("Authenticating user...", extra={"email": email})
    user = await get_user(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )
    if not verify_password(password, user.password):  # type:ignore
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authorized"
        )

    return user


async def get_current_user(token: str):
    try:
        payload = jwt.decode(token=token, key=SECRET, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if email is None:
            raise credentials_exception
    except ExpiredSignatureError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e
    except JWTError as e:
        raise credentials_exception from e
    user = await get_user(email=email)
    if user is None:
        raise credentials_exception
    return user
