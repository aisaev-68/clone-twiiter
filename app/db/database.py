from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.utils.logger import get_logger

logger = get_logger("db.database")


engine = create_async_engine(settings.async_db_uri) #echo=True

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
        logger.debug("ASYNC Pool: {pool}".format(pool=engine.pool.status()))
        yield session


async def init_db() -> None:
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

