from typing import Union
from fastapi import APIRouter, Depends, status

from crud.tweet import TweetService
from db.schemas import (
    Failure,
    NewTweetOut,
    Success,
    TweetIn,
    TweetsOut,
    UserOut,
)
from routers.user_current import current_user
from utils.errors import AppException, error_handler
from utils.logger import get_logger

logger = get_logger("routers.post")

router = APIRouter(
    prefix="/api/tweets",
    tags=["Tweets"],
)


@router.get(
    "",
    response_model=Union[TweetsOut, Failure],
    summary="Показать все твиты пользователей",
    description="Маршрут для отображения всех твитов.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def show_all_tweets(
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[TweetsOut, Failure]:
    """
    Endpoint для отображения всех твитов.

    :param user:
    :param service:
    :return: Объект согласно схеме TweetOut или Failure
    """
    logger.info("Получение всех твитов.")

    tweets = await service.get_all_tweets()

    return AppException(
        "id not found",
        "Пользователь с указанным id отсутствует в базе",
    ) if user is None else TweetsOut.parse_obj(
        {
            "result": True,
            "tweets": [tweet[0].to_json() for tweet in tweets],
        })


@router.post(
    "",
    response_model=Union[NewTweetOut, Failure],
    summary="Добавить новый твит пользователя",
    description="Маршрут для добавления нового твита пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def add_tweet(
        tweet: TweetIn,
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[NewTweetOut, Failure]:
    """
    Endpoint добавления нового твита пользователя.

    :param tweet: Объект полученный согласно схеме TweetIn
    :param user:
    :param service:
    :return: Объект согласно схеме NewTweetOut
    """
    logger.info("Добавления нового твита пользователя.")

    return AppException(
        "Tweet not found",
        "Tweet не найден",
    ) if user is None else NewTweetOut.parse_obj({
        "result": True,
        "tweet_id": (
            await service.add_new_tweet(
                tweet,
                user.id,
            )
        )["tweet_id"],
    })


@router.delete(
    "/{tweet_id}",
    summary="Удаляет твит с заданным ID",
    response_model=Union[Success, Failure],
    description="Маршрут для удаления твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def delete_tweet(
        tweet_id: int,
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[Success, Failure]:
    """
    Endpoint для удаления твита с заданным ID.

    :param tweet_id: ID твита для удаления
    :param user:
    :param service:
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление твита пользователя.")
    tweet = await service.get_tweet(user.id, tweet_id)

    AppException(
        "Tweet not found",
        "Tweet не найден",
    ) if tweet is None else await service.delete_tweet(tweet_id)

    return Success.parse_obj(
        {
            "result": True,
        },
    )
