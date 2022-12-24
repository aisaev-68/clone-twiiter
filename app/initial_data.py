import asyncio
from jose import jwt


from utils.logger import get_logger
from db.database import engine, Base, async_session
from db.models import User
from settings import settings

logger = get_logger("initial_data")


async def init_data():
    """
    Функция вызывается для создания тестовых данных.

    :return: None
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    logger.info("Добавление тестовых данных")

    session = async_session()
    session.add_all(
        [
            User(
                username="test",
                api_token=jwt.encode(
                    {"api-key": "test"},
                    settings.secret_key,
                    algorithm=settings.algorithm,
                )
            ),
            User(
                username="test1",
                api_token=jwt.encode(
                    {"api-key": "test1"},
                    settings.secret_key,
                    algorithm=settings.algorithm,
                )
            ),
            User(
                username="test2",
                api_token=jwt.encode(
                    {"api-key": "test2"},
                    settings.secret_key,
                    algorithm=settings.algorithm,
                )
            ),
            User(
                username="test3",
                api_token=jwt.encode(
                    {"api-key": "test3"},
                    settings.secret_key,
                    algorithm=settings.algorithm,
                )
            ),
        ]
    )
    await session.flush()
    await session.commit()

    logger.info("Тестовые данные добавлены!")

    await engine.dispose()

if __name__ == '__main__':
    asyncio.run(init_data())