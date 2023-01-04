from pathlib import Path
from typing import List, Optional, Union

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.db.database import get_db
from app.db.models import Media, Tweet, TweetLikes
from app.schema.schemas import NewTweetOut, Success, TweetIn, TweetsOut
from app.utils.logger import get_logger

logger = get_logger("crud.post")


class TweetService:
    """
    Сервис обработки Endpoint связанных с пользователями
    """

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    # , selectionload=None
    async def get_all_tweets(self):
        """
        Метод для получения всех твитов из базы.
        :param user_id:
        :return: Объект согласно схеме TweetsOut или Failure
        """

        result = await self.session.execute(
            select(Tweet).order_by(Tweet.created_at.desc()).options(
                selectinload(Tweet.likes),
                selectinload(Tweet.tweet_image),
                selectinload(Tweet.user)))
        posts = result.all()

        return posts

    async def get_tweet(
            self,
            user_id: int,
            tweet_id: int,
    ) -> Union[Tweet, None]:
        """
        Метод для получения всех твита из базы.
        :param user_id:
        :param post_id:
        :return: Объект согласно схеме TweetsOut или Failure
        """

        result = await self.session.execute(
            select(Tweet).where(
                Tweet.user_id == user_id,
                Tweet.id == tweet_id
            ))
        tweet: Union[Tweet, None] = result.scalars().first()

        return tweet

    async def add_new_tweet(
            self,
            tweet: TweetIn,
            user_id: int,
    ):
        """
        Метод обработки нового твита.

        :param post: Информация полученная с фронта согласно схеме TweetIn
        :param user_id: ID пользователя отправившего твит
        :param: file:
        :return: Объект согласно схеме TweetSuccess
        """
        new_tweet: Optional[Tweet] = Tweet(
            content=tweet.tweet_data,
            user_id=user_id,
        )

        self.session.add(new_tweet)
        await self.session.flush()
        await self.session.commit()

        for tweet_id in tweet.tweet_media_ids:
            result = await self.session.execute(select(Media).where(Media.id == tweet_id))
            media: Optional[Media] = result.scalars().first()
            if media is not None:
                media.tweet_id = new_tweet.id
                await self.session.flush()
                await self.session.commit()

        return {"tweet_id": new_tweet.id}

    async def delete_tweet(self, tweet_id: int) -> None:
        """
        Метод для удаления твита пользователя.

        :param tweet_id: ID твита для удаления
        :param user_id: ID пользователя, который хочет удалить твит
        :return: Объект согласно схеме Success или Failure
        """
        all_medias = await self.session.execute(
            select(Media).where(
                Media.tweet_id == tweet_id
            ))
        media: List[Media] = all_medias.scalars().all()

        if media is not None:
            for tweet_file in media:
                await self.session.execute(delete(Media).where(Media.tweet_id == tweet_file.tweet_id))
                file_path = Path(str(tweet_file.path_file))
                file_path.unlink()
        await self.session.execute(
            delete(TweetLikes).where(TweetLikes.tweet_id == tweet_id))
        # , TweetLikes.user_id == user_id
        await self.session.execute(delete(Tweet).where(Tweet.id == tweet_id))
        await self.session.commit()

    async def add_like(
            self,
            tweet_id: int,
            user_id: int,
    ):
        """
        Метод для добавления лайка с твита пользователя.

        :param tweet_id: ID твита на который нужно поставить
        :param user_id: ID пользователя которых хочет поставить
        :return: Объект согласно схеме Success или Failure
        """
        new_like = TweetLikes(tweet_id=tweet_id, user_id=user_id)
        self.session.add(new_like)
        await self.session.flush()
        await self.session.commit()

        return Success.parse_obj({"result": True})

    async def delete_like(
            self,
            tweet_id: int,
            user_id: int,
    ):
        """
        Метод для удаления лайка с твита пользователя.

        :param tweet_id: ID твита на который нужно поставить/удалить лайк
        :param user_id: ID пользователя которых хочет поставить/удалить лайк
        :return: Объект согласно схеме Success или Failure
        """
        query = delete(TweetLikes).where(
            TweetLikes.user_id == user_id,
            TweetLikes.tweet_id == tweet_id,
        )
        await self.session.execute(query)
        await self.session.commit()
