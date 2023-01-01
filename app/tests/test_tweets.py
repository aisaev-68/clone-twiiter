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
        "tweet_id": 2,
    }


@pytest.mark.asyncio
async def test_delete_tweets(client: AsyncClient):
    response = await client.delete(
        "/api/tweets/1",
        headers={"api-key": "test"},
    )
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
    }

@pytest.mark.asyncio
async def test_delete_tweets_other_user(client: AsyncClient):
    res = (await client.post(
        "/api/tweets",
        json={
            "tweet_data": "Чужой твит",
            "tweet_media_ids": [1],
        },
        headers={"api-key": "test1"},
    ))
    id_tweet = res.json()["tweet_id"]
    response = await client.delete(
        f"/api/tweets/{id_tweet}",
        headers={"api-key": "test"},
    )
    assert response.status_code == 422
    assert response.json() == {
        "result": False,
        "error_type": "Tweet not found",
        "error_message": "Tweet не найден",
    }