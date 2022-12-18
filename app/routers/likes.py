from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from utils.get_token_header import get_apikey_header
from utils.logger import get_logger
from db.models import Tweets, Users
from db.schemas import Success

logger = get_logger("routers.likes")

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
async def delete_like(
        tweet_id: int,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
) -> Success:
    """
    Endpoint для удаления лайка твиту с заданным ID.

    :param tweet_id: ID твита для удаления лайка
    :param api_key:
    :param session: AsyncSession
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление лайка пользователя.")
    result = await Users.get_user_by_token(session, api_key)
    user = result.dict()

    response = await Tweets.delete_like(
        session, tweet_id,
        user["user"]["id"],
    )
    return response


@router.post(
    "/{tweet_id}/likes",
    summary="Добавляет лайк твиту с заданным ID",
    response_model=Success,
    description="Маршрут для добавления лайка твиту с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
async def like_tweet(
        tweet_id: int,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
) -> Success:
    """
    Endpoint для добавления лайка твиту с заданным ID.

    :param tweet_id: ID твита для добавления лайка
    :param api_key:
    :param session: AsyncSession
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Добавление лайка пользователя.")
    result = await Users.get_user_by_token(session, api_key)
    user = result.dict()
    print(1111, user)
    response = await Tweets.add_like(
        session, tweet_id,
        user["user"]["id"],
    )

    return response
