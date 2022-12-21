from typing import Dict

from fastapi import APIRouter, Depends, status


from utils.logger import get_logger
from db.schemas import Success, UserOut, Failure
from crud.user import UserService
from routers.user_current import current_user
from utils.errors import AppException, error_handler

logger = get_logger("routers.user")

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
@error_handler
async def get_user_profile(
        user: current_user = Depends(),
) -> UserOut | Failure:
    """
    Маршрут получения информации о текущем пользователе.

    :param user:
    :return: Объект согласно схеме UserOut
    """
    logger.info(
        "Получение информации о текущем пользователе.",
    )


    if user.api_token is None:
        logger.error("Пользователь не ввел api-key млм пользователь с указанным api-key отсутствует в базе")
        raise AppException(
            "api-key not found",
            "Пользователь с указанным api-key отсутствует в базе",
        )

    response = {"result": True,
                "user": user.to_json(),
                }
    return UserOut.parse_obj(response)


@router.get(
    "/{user_id}",
    response_model=UserOut,
    summary="Показывает данные пользователя по id",
    description="Маршрут получения информации о пользователе по ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def get_user(
        user_id: int,
        service: UserService = Depends(),
) -> UserOut | Failure:
    """
    Маршрут получения информации о пользователе по ID.

    :param user_id: ID пользователя для получения информация.
    :param service:
    :return: Объект согласно схеме UserOut
    """
    logger.info(
        "Получение информации о пользователе с идентификатором {user_id}.",
    )
    user = await service.get_user_info(user_id)
    if user is None:
        logger.error("Пользователь с указанным id отсутствует в базе")
        raise AppException(
            "id not found",
            "Пользователь с указанным id отсутствует в базе",
        )

    response = {"result": True,
                "user": user.to_json(),
                }
    return UserOut.parse_obj(response)


@router.delete(
    "/{user_id}/follow",
    summary="Подписывает на пользователя",
    response_model=Success,
    description="Маршрут - позволяет подписаться на другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
# @router.post(
#     "/{user_id}/follow",
#     summary="Подписывает на пользователя",
#     response_model=Success,
#     description="Маршрут - позволяет подписаться на другого пользователя.",
#     response_description="Успешный ответ",
#     status_code=status.HTTP_201_CREATED,
# )
@error_handler
async def add_following(
        user_id: int,
        user: Dict = Depends(current_user),
        service: UserService = Depends(),
) -> Success | Failure:
    """
    Маршрут - позволяет подписаться на другого пользователя.

    :param user_id: ID пользователя на которого необходимо подписаться
    :param user:
    :param service:
    :return: Объект согласно схеме Success или Failure
    """

    response = await service.follow(user_id, user["user"]["id"])

    return Success.parse_obj(response)


@router.post(
    "/{user_id}/follow",
    summary="Отписывает от пользователя",
    response_model=Success,
    description="Маршрут - позволяет отписаться от другого пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
# @router.delete(
#     "/{user_id}/follow",
#     summary="Отписывает от пользователя",
#     response_model=Success,
#     description="Маршрут - позволяет отписаться от другого пользователя.",
#     response_description="Успешный ответ",
#     status_code=status.HTTP_200_OK,
# )
@error_handler
async def delete_following(
        user_id: int,
        user: Dict = Depends(current_user),
        service: UserService = Depends(),
) -> Success | Failure:
    """
    Маршрут - позволяет отписаться от другого пользователя.

    :param user_id: ID пользователя от которого необходимо отписаться
    :param user:
    :param service: Сервис для обработки маршрута
    :return: Объект согласно схеме Success или Failure
    """
    response = await service.unfollow(user_id, user["user"]["id"])

    return Success.parse_obj(response)
