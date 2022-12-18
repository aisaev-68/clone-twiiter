"""db module."""
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from utils.logger import get_logger
from settings import DATABASE_URL

logger = get_logger("routers.tweets")

# DATABASE_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
#     settings.db_user,
#     settings.db_password,
#     settings.db_host,
#     settings.db_port,
#     settings.db_name,
# )

engine = create_async_engine(DATABASE_URL, echo=True)

Base = declarative_base()

async_session = sessionmaker(
    engine,
    expire_on_commit=False,
    class_=AsyncSession,
)


async def get_db() -> AsyncGenerator:
    """
    Генерирует сессию.

    :yield: AsyncGenerator
    """
    async with async_session() as session:
        logger.debug(f"ASYNC Pool: {engine.pool.status()}")
        yield session

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)