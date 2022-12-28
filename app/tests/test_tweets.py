import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_tweets(client: AsyncClient):
    response = await client.get("/api/tweets", headers={"api-key": "test"})
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_add_tweets(client: AsyncClient):
    response = await client.post(
        "/api/tweets",
        json={
            "tweet_data": "Мой твит",
            "tweet_media_ids": [1],
        },
        headers={"api-key": "test"},
    )
    assert response.status_code == 201
    assert response.json() == {
        "result": True,
        "tweet_id": 1,
    }


@pytest.mark.asyncio
async def test_delete_tweets(client: AsyncClient):
    response = await client.post(
        "/api/tweets/1",
        headers={"api-key": "test"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
    }
