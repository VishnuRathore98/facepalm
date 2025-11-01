import pytest
from httpx import AsyncClient


async def create_comment(
        body: str, post_id: str, async_client: AsyncClient
) -> dict:
    response = await async_client.post(
        "/comment", 
        json={"body": body, "post_id": post_id}
    )
    return response.json()


@pytest.fixture()
async def created_comment(async_client: AsyncClient, create_post: dict):
    return await create_comment(
        body="test comment", 
        post_id=create_post['id'], 
        async_client=async_client
    )
