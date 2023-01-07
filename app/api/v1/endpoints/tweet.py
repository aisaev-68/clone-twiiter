from typing import Union

from fastapi import APIRouter, Depends, status

from app.api import depends
from app.crud.tweet import TweetService
from app.schema.schemas import (
    Failure,
    NewTweetOut,
    Success,
    TweetIn,
    TweetsOut,
    UserOut,
)
from app.utils.errors import AppException, error_handler
from app.utils.logger import get_logger

logger = get_logger("endpoints.post")

router = APIRouter()


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
        user: depends.current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[TweetsOut, Failure]:
    """
    Endpoint для отображения всех твитов.

    :param user: текущий пользователь
    :param service: сервис обработки Tweet
    :return: Объект согласно схеме Union[TweetsOut, Failure]
    """
    logger.info("Получение всех твитов.")

    tweets = await service.get_all_tweets()
    print(tweets)
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
        user: depends.current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[NewTweetOut, Failure]:
    """
    Endpoint добавления нового твита пользователя.

    :param tweet: Объект полученный согласно схеме TweetIn
    :param user: текущий пользователь
    :param service: сервис обработки Tweet
    :return: Объект согласно схеме Union[NewTweetOut, Failure]
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
        )["id"],
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
        user: depends.current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[Success, Failure]:
    """
    Endpoint для удаления твита с заданным ID.

    :param tweet_id: ID твита для удаления
    :param user: текущий пользователь
    :param service: сервис обработки Tweet
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


@router.delete(
    "/{tweet_id}/likes",
    summary="Удаляет лайк твита с заданным ID",
    response_model=Union[Success, Failure],
    description="Маршрут для удаления лайка твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
)
@error_handler
async def delete_like(
        tweet_id: int,
        user: depends.current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[Success, Failure]:
    """
    Endpoint для удаления лайка твиту с заданным ID.

    :param tweet_id: ID твита для удаления лайка
    :param user: текущий пользователь
    :param service:
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление лайка пользователя.")
    AppException(
        "id not found",
        "Пользователь с указанным id отсутствует в базе",
    ) if user is None else await service.delete_like(
        tweet_id,
        user.id,
    )
    return Success.parse_obj(
        {
            "result": True,
        },
    )


@router.post(
    "/{tweet_id}/likes",
    summary="Добавляет лайк твиту с заданным ID",
    response_model=Union[Success, Failure],
    description="Маршрут для добавления лайка твиту с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def like_tweet(
        tweet_id: int,
        user: depends.current_user = Depends(),
        service: TweetService = Depends(),
) -> Union[Success, Failure]:
    """
    Endpoint для добавления лайка твиту с заданным ID.

    :param tweet_id: ID твита для добавления лайка
    :param user:
    :param service: AsyncSession
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Добавление лайка пользователя.")
    AppException(
        "id not found",
        "Пользователь с указанным id отсутствует в базе",
    ) if user is None else await service.add_like(
        tweet_id,
        user.id,
    )

    return Success.parse_obj(
        {
            "result": True,
        },
    )

