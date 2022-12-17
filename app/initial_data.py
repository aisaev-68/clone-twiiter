from logger.logger import get_logger
from db.database import Base, async_session, engine
from models.models import Users

logger = get_logger("app_events")

async def init_data() -> None:
    """
    Функция вызывается для создания тестовых данных.

    :return: None
    """
    logger.info("ДОбавление тестовых данных")
    session = async_session()
    await Users.add_users(session)

if __name__ == '__main__':
    init_data()
