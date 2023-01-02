import asyncio
import os

from jose import jwt

from app.db.database import async_session
from app.db.models import User

from app.utils.logger import get_logger

logger = get_logger("initial_data")

algorithm: str = os.getenv("ALGORITHM", "")
secret_key: str = os.getenv("SECRET_KEY", "")


async def init_data():
    """
    Функция вызывается для создания тестовых данных.

    :return: None
    """

    logger.info("Добавление тестовых данных")

    session = async_session()
    session.add_all(
        [
            User(
                username="test",
                api_token=jwt.encode(
                    claims={"api-key": "test"},
                    key=secret_key,
                    algorithm=algorithm,
                )
            ),
            User(
                username="test1",
                api_token=jwt.encode(
                    claims={"api-key": "test1"},
                    key=secret_key,
                    algorithm=algorithm,
                )
            ),
            User(
                username="test2",
                api_token=jwt.encode(
                    claims={"api-key": "test2"},
                    key=secret_key,
                    algorithm=algorithm,
                )
            ),
            User(
                username="test3",
                api_token=jwt.encode(
                    claims={"api-key": "test3"},
                    key=secret_key,
                    algorithm=algorithm,
                )
            ),
        ]
    )
    await session.flush()
    await session.commit()

    logger.info("Тестовые данные добавлены!")

    # await engine.dispose()


if __name__ == '__main__':
    asyncio.run(init_data())
