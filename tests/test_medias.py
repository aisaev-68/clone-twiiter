import aiofiles
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_add_media(client: AsyncClient):

    async with aiofiles.open("app/images/1.jpg", mode="rb") as img_file:
        data = await img_file.read()

    response = await client.post("/api/medias", files={"file": data}, headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json() == {
        "result": True,
        "media_id": 1,
    }
