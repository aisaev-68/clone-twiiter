from typing import List, Optional, Union

from fastapi import Depends
from sqlalchemy import delete, desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.config import settings
from app.db.database import get_db
from app.db.models import Media, Tweet, TweetLikes
from app.schema.schemas import Success, TweetIn, TweetsOut, TweetSuccess
from app.utils.logger import get_logger

logger = get_logger("crud.post")


class TweetService:
    """Сервис обработки Endpoint связанных с пользователями"""
    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_all_tweets(self) -> List[Tweet]:
        """
        Метод для получения всех твитов из базы.

        :return: Объект согласно схеме List[Tweet]
        """
        result = await self.session.execute(
            select(Tweet).order_by(desc(Tweet.created_at)).options(
                selectinload(Tweet.likes),
                selectinload(Tweet.tweet_image),
                selectinload(Tweet.user)))
        tweets = result.all()

        return tweets

    async def get_tweet(
            self,
            user_id: int,
            tweet_id: int,
    ) -> Optional[Tweet]:
        """
        Метод для получения всех твита из базы.
        :param user_id: id пользователя
        :param tweet_id: id tweet
        :return: Объект согласно схеме Union[Tweet]
        """
        result = await self.session.execute(
            select(Tweet).where(
                Tweet.user_id == user_id,
                Tweet.id == tweet_id
            ))
        tweet = result.scalars().first()

        return tweet

    async def add_new_tweet(
            self,
            tweet: TweetIn,
            user_id: int,
    ) -> Optional[Tweet]:
        """
        Метод обработки нового твита.

        :param tweet: Информация полученная с фронта согласно схеме TweetIn
        :param user_id: ID пользователя отправившего твит
        :return: Объект Optional[Tweet]
        """
        new_tweet = Tweet(
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

        return new_tweet

    async def delete_tweet(self, tweet_id: int) -> None:
        """
        Метод для удаления твита пользователя.

        :param tweet_id: ID твита для удаления
        :param user_id: ID пользователя, который хочет удалить твит
        :return: Объект None
        """
        all_medias = await self.session.execute(
            select(Media).where(
                Media.tweet_id == tweet_id
            ))
        media: List[Media] = all_medias.scalars().all()

        if media is not None:
            for tweet_file in media:
                await self.session.execute(delete(Media).where(Media.tweet_id == tweet_file.tweet_id))
                file_path = settings.path_image() / tweet_file.path_file.split("/")[1]
                file_path.unlink()
        await self.session.execute(
            delete(TweetLikes).where(TweetLikes.tweet_id == tweet_id))
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
    ) -> None:
        """
        Метод для удаления лайка с твита пользователя.

        :param tweet_id: ID твита на который нужно поставить/удалить лайк
        :param user_id: ID пользователя которых хочет поставить/удалить лайк
        :return: Объект согласно схеме None
        """
        query = delete(TweetLikes).where(
            TweetLikes.user_id == user_id,
            TweetLikes.tweet_id == tweet_id,
        )
        await self.session.execute(query)
        await self.session.commit()
