import pytest
from httpx import AsyncClient
from routers.tweets import router


@pytest.mark.anyio
async def test_get_tweets():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        response = await ac.get("/api/tweets", headers={"api-key": "test"})
        assert response.status_code == 200


@pytest.mark.anyio
async def test_add_tweets():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        response = await ac.post(
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


@pytest.mark.anyio
async def test_delete_tweets():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        response = await ac.post(
            "/api/tweets/1",
            headers={"api-key": "test"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "result": True,
            }
