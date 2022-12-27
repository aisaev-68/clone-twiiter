from typing import AsyncGenerator
import asyncio
import pytest
from httpx import AsyncClient
import pytest_asyncio
from db.database import get_db
from main import app


@pytest_asyncio.fixture
# @pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0:8080") as async_client:
        yield async_client


# @pytest.yield_fixture
# async def init_db() -> AsyncGenerator:
#     """
#     Генерирует сессию.
#
#     :yield: AsyncGenerator
#     """
#     async with get_db() as db:
#         yield db