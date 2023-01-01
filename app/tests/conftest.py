import asyncio

from httpx import AsyncClient
import pytest
from main import app


@pytest.fixture(scope="session")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.yield_fixture(scope="session")
async def client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080") as async_client:
        yield async_client
