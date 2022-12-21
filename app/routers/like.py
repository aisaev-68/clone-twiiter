from fastapi import APIRouter, Depends, status

from utils.logger import get_logger
from db.schemas import Success, Failure
from crud.post import PostService
from routers.user_current import current_user
from utils.errors import AppException, error_handler

logger = get_logger("routers.like")

router = APIRouter(
    prefix="/api/tweets",
    tags=["Likes"],
)

@router.delete(
    "/{post_id}/likes",
    summary="Удаляет лайк твита с заданным ID",
    response_model=Success,
    description="Маршрут для удаления лайка твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def delete_like(
        post_id: int,
        user: current_user = Depends(),
        service: PostService = Depends(),
) -> Success | Failure:
    """
    Endpoint для удаления лайка твиту с заданным ID.

    :param post_id: ID твита для удаления лайка
    :param user:
    :param service:
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление лайка пользователя.")
    if user is None:
        logger.error("Пользователь с указанным id отсутствует в базе")
        raise AppException(
            "id not found",
            "Пользователь с указанным id отсутствует в базе",
        )

    result = await service.get_user_by_token(user.api_token)
    user = result.dict()

    await service.delete_like(
        post_id,
        user["user"]["id"],
    )
    return Success.parse_obj({"result": True})


@router.post(
    "/{post_id}/likes",
    summary="Добавляет лайк твиту с заданным ID",
    response_model=Success,
    description="Маршрут для добавления лайка твиту с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def like_tweet(
        post_id: int,
        user: current_user = Depends(),
        service: PostService = Depends(),
) -> Success | Failure:
    """
    Endpoint для добавления лайка твиту с заданным ID.

    :param post_id: ID твита для добавления лайка
    :param user:
    :param service: AsyncSession
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Добавление лайка пользователя.")
    if user is None:
        logger.error("Пользователь с указанным id отсутствует в базе")
        raise AppException(
            "id not found",
            "Пользователь с указанным id отсутствует в базе",
        )

    await service.add_like(
        post_id,
        user.id,
    )

    return Success.parse_obj({"result": True})
