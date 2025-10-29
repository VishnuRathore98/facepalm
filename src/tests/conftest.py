from typing import AsyncGenerator, Generator
import pytest
from fastapi.testclient import TestClient
from src.main import app
from src.routers.post import post_table
from src.routers.comment import comment_table


@pytest.fixture(scope='session')
def anyio_backend():
    return 'asyncio'


@pytest.fixture()
def client() -> Generator:
    yield TestClient(app)

 
@pytest.fixture(autouse=True)
async def db() -> AsyncGenerator:
    post_table.clear()
    comment_table.clear()
    yield
