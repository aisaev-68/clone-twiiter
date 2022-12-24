import pytest
from httpx import AsyncClient
from routers.medias import router


@pytest.mark.anyio
async def test_add_tweets_likes():
    async with AsyncClient(app=router, base_url="http://0.0.0.0") as ac:
        with open("", mode="r", encoding="utf-8") as img_file:
            data = img_file.read()
        response = await ac.post("/api/medias", files=data, headers={"api-key": "test"})
        assert response.status_code == 201
        assert response.json() == {
            "result": True,
            "media_id": 1,
        }