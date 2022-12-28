import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_tweets_likes(client: AsyncClient):
    with open("", mode="r", encoding="utf-8") as img_file:
        data = img_file.read()
    response = await client.post("/api/medias", files=data, headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json() == {
        "result": True,
        "media_id": 1,
    }
