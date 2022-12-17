from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from utils.get_token_header import get_apikey_header
from utils.logger import get_logger
from db.models import Tweets, Users
from utils.schemas import NewTweetOut, Success, TweetIn, TweetsOut

logger = get_logger("routers.tweets")

router = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"],
)


@router.get(
    "",
    response_model=TweetsOut,
    summary="Показать все твиты пользователей",
    description="Маршрут для отображения всех твитов.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
    )
async def show_tweets(
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
        ) -> TweetsOut:
    """
    Endpoint для отображения всех твитов.

    :param api_key:
    :param session: AsyncSession
    :return: Объект согласно схеме TweetOut или Failure
    """
    logger.info("Получение всех твитов.")
    response = await Tweets.get_tweets(session, api_key)

    return response


@router.post(
    "",
    response_model=NewTweetOut,
    summary="Добавить новый твит пользователя",
    description="Маршрут для добавления нового твита пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
async def add_tweet(
        tweet: TweetIn,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
) -> NewTweetOut:
    """
    Endpoint добавления нового твита пользователя.

    :param tweet: Объект полученный согласно схеме TweetIn
    :param api_key: api-key пользователя
    :param session: AsyncSession
    :return: Объект согласно схеме NewTweetOut
    """
    logger.info("Добавления нового твита пользователя.")
    user = (await Users.get_user_by_token(session, api_key)).dict()
    response = await Tweets.add_new_tweet(
        session,
        tweet,
        int(user["user"]["id"]),
    )

    return response


@router.delete(
    "/{tweet_id}",
    summary="Удаляет твит с заданным ID",
    response_model=Success,
    description="Маршрут для удаления твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
    )
async def del_user_tweet(
        tweet_id: int,
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
        ) -> Success:
    """
    Endpoint для удаления твита с заданным ID.

    :param tweet_id: ID твита для удаления
    :param api_key:
    :param session: AsyncSession
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление твита пользователя.")
    user = (await Users.get_user_by_token(session, api_key)).dict()
    response = await Tweets.delete_tweet(session, tweet_id, user["user"]["id"])

    return response
