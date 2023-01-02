from typing import Union
from fastapi import (
    APIRouter,
    Depends,
    status,
)
from app.crud.user import UserService
from app.db.schemas import (
    Failure,
    Success,
    UserOut,
)
from app.routers.user_current import current_user
from app.utils.errors import (
    AppException,
    error_handler,
)
from app.utils.logger import get_logger

logger = get_logger("routers.user")

router = APIRouter(
    tags=["Users"],
)


@router.get(
    "/api/users/me",
    response_model=Union[UserOut, Failure],
    summary="Показывает данные текущего пользователя",
    description="Маршрут получения информации о текущем пользователе.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def get_user_profile(
        user: current_user = Depends(),
) -> Union[UserOut, Failure]:
    """
    Маршрут получения информации о текущем пользователе.

    :param user:
    :return: Объект согласно схеме UserOut
    """
    logger.info(
        "Получение информации о текущем пользователе.",
    )
    return (
        AppException(
            "api-key not found",
            "Пользователь с указанным api-key отсутствует в базе",
        ) if user is None else UserOut.parse_obj(
            {
                "result": True,
                "user": user.to_json(),
            },
        )
    )


@router.get(
    "/api/users/{user_id}",
    response_model=Union[UserOut, Failure],
    summary="Показывает данные пользователя по id",
    description="Маршрут получения информации о пользователе по ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def get_user(
        user_id: int,
        service: UserService = Depends(),
) -> Union[UserOut, Failure]:
    """
    Маршрут получения информации о пользователе по ID.

    :param user_id: ID пользователя для получения информация.
    :param service:
    :return: Объект согласно схеме Union[Success, Failure]
    """
    logger.info(
        "Получение информации о пользователе с идентификатором {id}.".format(
            id=user_id,
        ),
    )
    user_by_id = await service.get_user_info(user_id)
    return (
        AppException(
            "User not found",
            "Пользователь с указанным id отсутствует в базе",
        ) if user_by_id.api_token is None else UserOut.parse_obj(
            {
                "result": True,
                "user": user_by_id.to_json(),
            },
        )
    )


@router.delete(
    "/api/users/{user_id}/follow",
    summary="Подписывает на пользователя",
    response_model=Union[Success, Failure],
    description="Маршрут - позволяет подписаться на другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def add_following(
        user_id: int,
        user: current_user = Depends(),
        service: UserService = Depends(),
) -> Union[Success, Failure]:
    """
    Маршрут - позволяет подписаться на другого пользователя.

    :param user_id: ID пользователя на которого необходимо подписаться
    :param user:
    :param service:
    :return: Объект согласно схеме Success или Failure
    """
    result = await service.follow(user_id, user.id)

    return (
        AppException(
            "Followers not found",
            "Ошибка при подписке",
        ) if not result else Success.parse_obj(
            {
                "result": True,
            },
        )
    )


@router.delete(
    "/api/tweets/{user_id}/follow",
    summary="Отписывает от пользователя",
    response_model=Union[Success, Failure],
    description="Маршрут - позволяет отписаться от другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def delete_following(
        user_id: int,
        user: current_user = Depends(),
        service: UserService = Depends(),
) -> Union[Success, Failure]:
    """
    Маршрут - позволяет отписаться от другого пользователя.

    :param user_id: ID пользователя от которого необходимо отписаться
    :param user:
    :param service: Сервис для обработки маршрута
    :return: Объект согласно схеме Success или Failure
    """
    result = await service.unfollow(user_id, user.id)

    return (
        AppException(
            "Followers not found",
            "Пользователь не подписан",
        ) if not result else Success.parse_obj(
            {
                "result": True,
            },
        )
    )
