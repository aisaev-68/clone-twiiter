import pytest
from httpx import AsyncClient

api_key = "test"


@pytest.mark.asyncio
async def test_user_me(client: AsyncClient):
    response = await client.get("/api/users/me", headers={"api-key": "test"},)
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {"id": 1,
                 "name": "test",
                 "followers": [],
                 "following": []
                 }
    }


@pytest.mark.asyncio
async def test_user_by_id(client: AsyncClient):
    response = await client.get("/api/users/1", headers={"api-key": "test"})
    assert response.status_code == 200
    assert response.json() == {
        "result": True,
        "user": {
            "id": 1,
            "name": "test",
            "followers": [],
            "following": []
        }
    }


@pytest.mark.asyncio
async def test_to_follow(client: AsyncClient):
    response = await client.delete("/api/users/2/follow", headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json() == {
        "result": True
    }


@pytest.mark.asyncio
async def test_unfollow(client: AsyncClient):
    response = await client.delete("/api/tweets/2/follow", headers={"api-key": "test"})
    assert response.status_code == 201
    assert response.json() == {
        "result": True
    }

