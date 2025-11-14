import pytest
from httpx import AsyncClient


async def create_comment(body: str, post_id: str, async_client: AsyncClient) -> dict:
    response = await async_client.post(
        "/comment", json={"body": body, "post_id": post_id}
    )
    return response.json()


async def create_post(body: str, async_client: AsyncClient) -> dict:
    response = await async_client.post("/posts", json={"body": body})
    return response.json()


@pytest.fixture()
async def created_comment(async_client: AsyncClient, create_post: dict):
    return await create_comment(
        body="test comment", post_id=create_post["id"], async_client=async_client
    )


@pytest.mark.anyio
async def test_create_comment(async_client: AsyncClient, created_post: dict):
    body = "test comment"

    response = await async_client.post(
        "/comment", json={"body": body, "post_id": created_post["id"]}
    )
    assert response.status_code == 201
    assert {
        "id": response.json()["id"],
        "body": body,
        "post_id": created_post["id"],
    }.items() <= response.json().items()


@pytest.mark.anyio
async def test_get_comments_on_post(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")
    assert response.status_code == 200
    assert response.json() == [created_comment]


@pytest.mark.anyio
async def test_get_comments_on_empty_post(
    async_client: AsyncClient, created_post: dict
):
    response = await async_client.get(f"/post/{created_post['id']}/comment")

    assert response.status_code() == 200
    assert response.json() == []


@pytest.mark.anyio
async def test_get_post_with_comments(
    async_client: AsyncClient, created_post: dict, created_comment: dict
):
    response = await async_client.get(f"/post/{created_post['id']}")

    assert response.status_code() == 200
    assert response.json() == {"post": created_post, "comments": [created_comment]}
