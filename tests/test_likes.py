import pytest
from httpx import AsyncClient
from routers.likes import router


@pytest.mark.anyio
async def test_add_tweets_likes():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        response = await ac.post("/api/tweets/2/likes", headers={"api-key": "test"})
        assert response.status_code == 201
        assert response.json() == {
            "result": True,
            }


@pytest.mark.anyio
async def test_delete_tweets_likes():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        response = await ac.delete(
            "/api/tweets/2/likes",
            headers={"api-key": "test"},
        )
        assert response.status_code == 200
        assert response.json() == {
            "result": True,
            }
