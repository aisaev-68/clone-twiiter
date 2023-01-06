import asyncio
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker
from app.config import settings
from app.db.models import User, Base
from app.utils.logger import get_logger

logger = get_logger("initial_data")


async def init_data():
    """
    Функция вызывается для создания тестовых данных.

    :return: None
    """

    logger.info("Добавление тестовых данных")
    engine = create_async_engine(
        settings.async_db_uri,
        echo=True,
    )
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    users = [
        {"username": "test",
         "api_token": jwt.encode(
             claims={"api-key": "test"},
             key=settings.secret_key,
             algorithm=settings.algorithm, )
         },
        {
            "username": "test1",
            "api_token": jwt.encode(
                claims={"api-key": "test1"},
                key=settings.secret_key,
                algorithm=settings.algorithm, )
        },
        {
            "username": "test2",
            "api_token": jwt.encode(
                claims={"api-key": "test2"},
                key=settings.secret_key,
                algorithm=settings.algorithm, )
        },
        {
            "username": "test3",
            "api_token": jwt.encode(
                claims={"api-key": "test3"},
                key=settings.secret_key,
                algorithm=settings.algorithm, )
        },
    ]
    async with async_session() as session:
        async with session.begin():
            for user in users:
                session.add(User(**user))

    await engine.dispose()
    logger.info("Тестовые данные добавлены!")


if __name__ == '__main__':
    asyncio.run(init_data())
