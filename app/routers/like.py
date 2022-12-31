from crud.tweet import TweetService
from db.schemas import Failure, Success
from fastapi import APIRouter, Depends, status
from routers.user_current import current_user
from utils.errors import AppException, error_handler
from utils.logger import get_logger

logger = get_logger("routers.like")

router = APIRouter(
    prefix="/api/tweets",
    tags=["Likes"],
)

@router.delete(
    "/{tweet_id}/likes",
    summary="Удаляет лайк твита с заданным ID",
    response_model=Success,
    description="Маршрут для удаления лайка твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def delete_like(
        tweet_id: int,
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> Success | Failure:
    """
    Endpoint для удаления лайка твиту с заданным ID.

    :param tweet_id: ID твита для удаления лайка
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

    await service.delete_like(
        tweet_id,
        user.id,
    )
    return Success.parse_obj({"result": True})


@router.post(
    "/{tweet_id}/likes",
    summary="Добавляет лайк твиту с заданным ID",
    response_model=Success,
    description="Маршрут для добавления лайка твиту с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def like_tweet(
        tweet_id: int,
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> Success | Failure:
    """
    Endpoint для добавления лайка твиту с заданным ID.

    :param tweet_id: ID твита для добавления лайка
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
        tweet_id,
        user.id,
    )

    return Success.parse_obj({"result": True})