from typing import Callable

from logger.logger import get_logger
from db.database import Base, async_session, engine
from models.models import Users

logger = get_logger("app_events")


def create_start_app_handler() -> Callable:
    async def start_app() -> None:
        """
        Функция вызывается при старте приложения.

        :return: None
        """
        logger.info("Старт приложения")
        session = async_session()
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await Users.add_users(session)

    return start_app


def create_stop_app_handler() -> Callable:
    async def stop_app() -> None:
        """
        Функция вызывается при завершении работы приложения.

        :return: None
        """
        logger.info("Остановка приложения")
        await engine.dispose()

    return stop_app