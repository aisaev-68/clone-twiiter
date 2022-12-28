import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_tweets_likes(client: AsyncClient):
    response = await client.post("/api/tweets/2/likes", headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json() == {
        "result": True,
    }


@pytest.mark.asyncio
async def test_delete_tweets_likes(client: AsyncClient):
    response = await client.delete(
        "/api/tweets/2/likes",
        headers={"api-key": "test"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
    }
