from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from utils.get_token_header import get_apikey_header
from utils.logger import get_logger
from db.models import Users
from db.schemas import Success, UserOut

logger = get_logger("routers.users")

router = APIRouter(
    prefix="/api/users",
    tags=["Users"],
)


@router.get(
    "/me",
    response_model=UserOut,
    summary="Показывает данные текущего пользователя",
    description="Маршрут получения информации о текущем пользователе.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def get_user_profile(
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
) -> UserOut:
    """
    Маршрут получения информации о текущем пользователе.

    :param api_key: api-key
    :param session: AsyncSession
    :return: Объект согласно схеме UserOut
    """
    logger.info(
        "Получение информации о текущем пользователе.",
    )
    user = await Users.get_user_by_token(session, api_key)

    return UserOut.parse_obj(user)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Показывает данные пользователя по id",
    description="Маршрут получения информации о пользователе по ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def get_user(
        user_id: int,
        session: AsyncSession = Depends(get_db),
) -> UserOut:
    """
    Маршрут получения информации о пользователе по ID.

    :param user_id: ID пользователя для получения информация.
    :param session: AsyncSession
    :return: Объект согласно схеме UserOut
    """
    logger.info(
        "Получение информации о пользователе с идентификатором {user_id}.",
    )
    user = await Users.get_user_info(session, user_id)

    logger.info(user)

    return UserOut.parse_obj(user)


@router.post(
    "/{user_id}/follow",
    summary="Подписывает на пользователя",
    response_model=Success,
    description="Маршрут - позволяет подписаться на другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
async def add_following(
        user_id: int,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db)
) -> Success:
    """
    Маршрут - позволяет подписаться на другого пользователя.

    :param user_id: ID пользователя на которого необходимо подписаться
    :param api_key: api-key
    :param session: AsyncSession
    :return: Объект согласно схеме Success или Failure
    """
    user = (await Users.get_user_by_token(session, api_key)).dict()
    response = await Users.follow(session, user_id, user["user"]["id"])

    return Success.parse_obj(response)


@router.delete(
    "/{user_id}/follow",
    summary="Отписывает от пользователя",
    response_model=Success,
    description="Маршрут - позволяет отписаться от другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
async def delete_following(
        user_id: int,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db)
) -> Success:
    """
    Маршрут - позволяет отписаться от другого пользователя.

    :param user_id: ID пользователя от которого необходимо отписаться
    :param api_key: api-key
    :param session: Сервис для обработки маршрута
    :return: Объект согласно схеме Success или Failure
    """
    user = (await Users.get_user_by_token(session, api_key)).dict()
    response = await Users.unfollow(session, user_id, user["user"]["id"])

    return Success.parse_obj(response)
