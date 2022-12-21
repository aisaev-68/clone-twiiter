from typing import Union, List, Any, Dict, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import (
    delete,
    select,
)
from db.schemas import (
    Success,
    TweetsOut,
    NewTweetOut,
    TweetIn,
)
from utils.logger import get_logger
from db.models import Post, likes
from db.database import get_db

logger = get_logger("crud.post")


class PostService:
    """
    Сервис обработки Endpoint связанных с пользователями
    """

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def get_all_posts(self):
        """
        Метод для получения всех твитов из базы.
        :param user_id:
        :return: Объект согласно схеме TweetsOut или Failure
        """

        result = await self.session.execute(select(Post))
        posts = result.all()

        return posts

    async def get_post(
            self,
            user_id: int,
            post_id: int,
    ):
        """
        Метод для получения всех твита из базы.
        :param user_id:
        :param post_id:
        :return: Объект согласно схеме TweetsOut или Failure
        """

        result = await self.session.execute(select(Post).where(Post.user_id == user_id, Post.id == post_id))
        post = result.scalars().first()

        return post


    async def add_new_post(
            self,
            post: TweetIn,
            user_id: int,
    ):
        """
        Метод обработки нового твита.

        :param post: Информация полученная с фронта согласно схеме TweetIn
        :param user_id: ID пользователя отправившего твит
        :param: file:
        :return: Объект согласно схеме TweetSuccess
        """
        new_post = Post(
            content=post.tweet_data,
            user_id=user_id,
        )

        self.session.add(new_post)
        await self.session.flush()
        await self.session.commit()

        return new_post


    async def add_like(
            self,
            post_id: int,
            user_id: int,
    ):
        """
        Метод для добавления лайка с твита пользователя.

        :param post_id: ID твита на который нужно поставить
        :param user_id: ID пользователя которых хочет поставить
        :return: Объект согласно схеме Success или Failure
        """
        new_like = likes(post_id=post_id, user_id=user_id)
        self.session.add(new_like)
        await self.session.flush()
        await self.session.commit()

        return Success.parse_obj({"result": True})

    async def delete_like(
            self,
            post_id: int,
            user_id: int,
    ):
        """
        Метод для удаления лайка с твита пользователя.

        :param post_id: ID твита на который нужно поставить/удалить лайк
        :param user_id: ID пользователя которых хочет поставить/удалить лайк
        :return: Объект согласно схеме Success или Failure
        """
        query = delete(likes).where(
            likes.user_id == user_id,
            likes.post_id == post_id,
        )
        await self.session.execute(query)
        await self.session.commit()

    async def delete_post(self, post_id: int,) -> None:
        """
        Метод для удаления твита пользователя.

        :param post_id: ID твита для удаления
        :param user_id: ID пользователя, который хочет удалить твит
        :return: Объект согласно схеме Success или Failure
        """
        query = delete(Post).where(Post.id == post_id)
        print(555, query)
        await self.session.execute(query)
        await self.session.commit()



