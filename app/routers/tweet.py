from typing import Dict

from fastapi import APIRouter, Depends, status

from utils.logger import get_logger
from db.schemas import NewTweetOut, Success, TweetIn, TweetsOut, UserOut, Failure
from crud.tweet import TweetService
from routers.user_current import current_user
from utils.errors import AppException, error_handler

logger = get_logger("routers.post")

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
@error_handler
async def show_all_tweets(
        user: current_user = Depends(),
        service: TweetService = Depends(),
        ) -> TweetsOut | Failure:
    """
    Endpoint для отображения всех твитов.

    :param user:
    :param service:
    :return: Объект согласно схеме TweetOut или Failure
    """
    logger.info("Получение всех твитов.")
    if user is None:
        logger.error("Пользователь с указанным id отсутствует в базе")
        raise AppException(
            "id not found",
            "Пользователь с указанным id отсутствует в базе",
        )
    posts = await service.get_all_tweets()
    lst = []
    print(8888, posts) #8888 [(Post,), (Post,), (Post,), (Post,), (Post,)]
    for post in posts:
        obj = post[0].to_json()
        lst.append(obj)

    return TweetsOut.parse_obj({
        "result": True,
        "tweets": lst,
    })


@router.post(
    "",
    response_model=NewTweetOut,
    summary="Добавить новый твит пользователя",
    description="Маршрут для добавления нового твита пользователя.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def add_tweet(
        post: TweetIn,
        user: current_user = Depends(),
        service: TweetService = Depends(),
) -> NewTweetOut | Failure:
    """
    Endpoint добавления нового твита пользователя.

    :param post: Объект полученный согласно схеме TweetIn
    :param user:
    :param service:
    :return: Объект согласно схеме NewTweetOut
    """
    logger.info("Добавления нового твита пользователя.")
    new_post = await service.add_new_tweet(
        post,
        int(user.id),
    )

    return NewTweetOut.parse_obj({
        "result": True,
        "tweet_id": new_post.id,
    })


@router.delete(
    "/{post_id}",
    summary="Удаляет твит с заданным ID",
    response_model=Success,
    description="Маршрут для удаления твита с заданным ID.",
    response_description="Успешный ответ",
    status_code=status.HTTP_200_OK,
    )
@error_handler
async def del_user_tweet(
        post_id: int,
        user: current_user = Depends(),
        service: TweetService = Depends(),
        ) -> Success | Failure:
    """
    Endpoint для удаления твита с заданным ID.

    :param post_id: ID твита для удаления
    :param user:
    :param service:
    :return: Возвращает объект согласно схеме Success или Failure
    """
    logger.info("Удаление твита пользователя.")
    tweet = await service.get_tweet(user.id, post_id)
    print(7777, tweet)
    if tweet is not None:
        if tweet.user_id == user.id:
            await service.delete_tweet(post_id)
        else:
            logger.error(f"Пользователь с {user.id} пытается удалить чужой пост")
            raise AppException(
                "User not delete post",
                "Пользователь с указанным id не может удалить пост",
            )

    else:
        logger.error("Пост не найден")
        raise AppException(
            "Tweet not found",
            "Пост не найден",
        )

    return Success.parse_obj({"result": True})

