from typing import AsyncGenerator, Generator
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient, ASGITransport
import os

os.environ["ENV_STATE"] = "test"


from src.database import database, user_table  # noqa:E402
from src.main import app  # noqa:E402


@pytest.fixture(scope="session")
def anyio_backend():
    return "asyncio"


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)


@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    await database.connect()
    yield
    await database.disconnect()


@pytest.fixture()
async def async_client(client):
    transport = ASGITransport(app=app)
    async with AsyncClient(
        transport=transport,
        base_url=client.base_url,
    ) as ac:
        yield ac


@pytest.fixture()
async def registered_user(async_client: AsyncClient) -> dict:
    user_details = {"email": "test@mail.com", "password": "12345678"}
    await async_client.post("/register", json=user_details)
    query = user_table.select().where(
        user_table.c.email == user_details["email"],
    )
    user = await database.fetch_one(query)
    user_details["id"] = user.id  # type: ignore
    return user_details


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_post(async_client: AsyncClient):
    return await create_post("Test post", async_client)
