from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient

from app.db.database import get_db
from app.main import app


@pytest.fixture()
async def client():
    async with AsyncClient(app=app, base_url="http://0.0.0.0") as async_client:
        yield async_client


@pytest.yield_fixture
async def init_db() -> AsyncGenerator:
    """
    Генерирует сессию.

    :yield: AsyncGenerator
    """
    async with get_db() as db:
        yield db