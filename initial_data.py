import asyncio
import os
from dotenv import load_dotenv
from jose import jwt

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine

from sqlalchemy.orm import sessionmaker

from app.db.models import User
from app.utils.logger import get_logger

logger = get_logger("initial_data")

load_dotenv()

secret_key = os.getenv("SECRET_KEY")
algorithm = os.getenv("ALGORITHM")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_NAME = os.getenv("DB_NAME")

asyncpg_url: str = f"postgresql+asyncpg://{DB_USER}:" \
                   f"{DB_PASSWORD}@" \
                   f"{DB_HOST}:5432/{DB_NAME}"

async def init_data():
    """
    Функция вызывается для создания тестовых данных.

    :return: None
    """

    logger.info("Добавление тестовых данных")
    engine = create_async_engine(
        asyncpg_url,
        echo=True,
    )

    async_session = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

    users = [
        {"username": "test",
         "api_token": jwt.encode(
             claims={"api-key": "test"},
             key=secret_key,
             algorithm=algorithm, )
         },
        {
            "username": "test1",
            "api_token": jwt.encode(
                claims={"api-key": "test1"},
                key=secret_key,
                algorithm=algorithm, )
        },
        {
            "username": "test2",
            "api_token": jwt.encode(
                claims={"api-key": "test2"},
                key=secret_key,
                algorithm=algorithm, )
        },
        {
            "username": "test3",
            "api_token": jwt.encode(
                claims={"api-key": "test3"},
                key=secret_key,
                algorithm=algorithm, )
        },
    ]
    async with async_session() as session:
        async with session.begin():
            for user in users:
                session.add(User(**user))


    logger.info("Тестовые данные добавлены!")



if __name__ == '__main__':
    asyncio.run(init_data())
