import pytest
from jose import jwt

from src import security


@pytest.mark.anyio
async def test_get_user(registered_user: dict):
    user = await security.get_user(registered_user["email"])

    assert user.email == registered_user["email"]  # type: ignore


@pytest.mark.anyio
async def test_get_user_not_found():
    user = await security.get_user("test@mail.com")
    assert user is None


def test_password_hashes():
    password = "test123"
    assert security.verify_password(password, security.get_password_hash(password))


def test_access_token_expiry_minutes():
    assert security.access_token_exp_min() == 30


def test_create_access_token():
    token = security.create_access_token(email="test@mail.com")
    assert {"sub": "test@mail.com"}.items() <= jwt.decode(
        token, key=security.SECRET, algorithms=[security.ALGORITHM]
    ).items()


@pytest.mark.anyio
async def test_authenticate_user(registered_user: dict):
    user = await security.authenticate_user(
        registered_user["email"], registered_user["password"]
    )
    assert user.email == registered_user["email"]  # type: ignore


@pytest.mark.anyio
async def test_authenticate_user_not_found():
    with pytest.raises(security.HTTPException):
        await security.authenticate_user(email="test@mail.net", password="test")


@pytest.mark.anyio
async def test_authenticate_user_wrong_password(registered_user: dict):
    with pytest.raises(security.HTTPException):
        await security.authenticate_user(
            email=registered_user["email"], password="4321"
        )
