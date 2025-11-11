import pytest
from httpx import AsyncClient

from src import security


async def register_user(async_client: AsyncClient, email: str, password: str):
    return await async_client.post(
        "/register",
        json={
            "email": email,
            "password": password,
        },
    )


async def test_password_hashing():
    password = "test123"
    assert security.verify_password(
        password,
        security.get_password_hash(password),
    )


@pytest.mark.anyio
async def test_register_user(async_client: AsyncClient):
    response = await register_user(async_client, "test@mail.com", "test123")
    assert response.status_code == 201


@pytest.mark.anyio
async def test_already_registered_user(
    async_client: AsyncClient,
    registered_user: dict,
):
    response = await register_user(
        async_client,
        registered_user["email"],
        registered_user["password"],
    )
    assert response.status_code == 400
