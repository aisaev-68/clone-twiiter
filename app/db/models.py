import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiofiles
from fastapi import UploadFile
from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    Text,
    delete,
    select,
)
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import relationship, selectinload

from db.database import Base
from utils.logger import get_logger
from db.schemas import (
    FileSuccess,
    NewTweetOut,
    Success,
    TweetIn,
    TweetsOut,
    UserOut,
)
from settings import settings, uploaded_file_path
from utils.errors import AppException, error_handler


logger = get_logger("routers.users")


class Users(Base):
    __tablename__ = "users"
    id: int = Column(Integer(), primary_key=True)
    username: str = Column(String(), nullable=False)
    api_token: str = Column(Text(), nullable=False)
    following: List["Users"] = relationship(
        "Users",
        secondary="followings",
        primaryjoin="Users.id == Followings.user_id",
        secondaryjoin="Users.id == Followings.user_to_follow_id",
        back_populates="followers",
        lazy="selectin",
        uselist=True,
    )
    followers: List["Users"] = relationship(
        "Users",
        secondary="followings",
        primaryjoin="Users.id == Followings.user_to_follow_id",
        secondaryjoin="Users.id == Followings.user_id",
        back_populates="following",
        lazy="selectin",
        uselist=True,
    )

    @classmethod
    async def get_all_users(
            cls,
            session: AsyncSession,
    ) -> Union[List[Any], Dict[str, Any]]:
        """
        Метод возвращает всех пользователей из базы.

        :param session: AsyncSession
        :return: список объектов Users
        """
        users = await session.execute(select(cls))

        return users.scalars().all()

    @classmethod
    @error_handler
    async def get_user_info(
            cls,
            session: AsyncSession,
            user_id: int = None,
    ) -> UserOut:
        """
        Метод для получения информации о пользователе.

        :param session: AsyncSession
        :param user_id: ID пользователя о котором необходимо
        получить информацию.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(cls).where(cls.id == user_id).options(
            selectinload(cls.followers),
            selectinload(cls.following),
        )

        result = await session.execute(query)
        user = result.scalars().first()

        if user is None:
            logger.error("Пользователь с указанным id отсутствует в базе")
            raise AppException(
                "id not found",
                "Пользователь с указанным id отсутствует в базе",
            )

        response = {"result": True,
                    "user": user.to_json(),
                    }
        return UserOut.parse_obj(response)

    @classmethod
    @error_handler
    async def get_user_by_id(cls, session: AsyncSession, user_id: int) -> UserOut:
        """
        Метод - получает информацию о пользователе по его ID.

        :param session: AsyncSession
        :param user_id: ID пользователя.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(cls).where(
            cls.id == user_id
        ).options(selectinload(cls.followers),
                  selectinload(cls.following),
                  )
        result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            logger.error("Пользователь с указанным id отсутствует в базе")
            raise AppException(
                "id not found",
                "Пользователь с указанным id отсутствует в базе",
            )

        response = {"result": True,
                    "user": user.to_json(),
                    }
        return UserOut.parse_obj(response)

    @classmethod
    @error_handler
    async def get_user_by_token(
            cls,
            session: AsyncSession,
            api_key: str,
    ) -> UserOut:
        """
        Метод получает информацию о пользователе по его ID.

        :param session: AsyncSession
        :param api_key: api-key.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(cls).where(
            cls.api_token == api_key).options(
            selectinload(cls.followers),
            selectinload(cls.following),
        )
        logger.info("Получение информации о текущем пользователе.")
        result = await session.execute(query)
        user = result.scalars().first()

        if user is None:
            logger.error("Пользователь с указанным api-key отсутствует в базе")
            raise AppException(
                "api-key not found",
                "Пользователь с указанным api-key отсутствует в базе",
            )

        response = {"result": True,
                    "user": user.to_json(),
                    }
        return UserOut.parse_obj(response)

    @classmethod
    @error_handler
    async def follow(
            cls,
            session: AsyncSession,
            user_to_follow: int,
            current_user_id: int,
    ) -> Success:
        """
        Метод для добавления пользователя в подписки и удаления из них.

        :param session: AsyncSession
        :param user_to_follow: ID пользователя на которого необходимо подписаться
        :param current_user_id: ID пользователя который подписывается
        :return: Объект согласно схеме Success или Failure
        """
        result = await session.execute(
            select(cls).options(
            selectinload(cls.followers),
                selectinload(cls.following),
            ),
        )

        to_follow: Optional[Users] = result.scalars().first()
        if to_follow is not None:
            following_id: List[int] = [user.id for user in to_follow.following]
        else:
            following_id = []

        if user_to_follow not in following_id:
            session.add(
                Followings(
                    user_id=current_user_id,
                    user_to_follow_id=user_to_follow,
                ),
            )
            await session.flush()
            await session.commit()
        else:
            logger.error("Пользователь с указанным id уже подписан")
            raise AppException(
                "Wrong add follower",
                "Пользователь с указанным id уже подписан",
            )

        return Success.parse_obj({"result": True})

    @classmethod
    @error_handler
    async def unfollow(
            cls,
            session: AsyncSession,
            user_to_follow: int,
            current_user_id: int,
    ) -> Success:
        """
        Метод для удаления пользователя из подписки.

        :param session: AsyncSession
        :param user_to_follow: ID пользователя от которого необходимо отписаться
        :param current_user_id: ID пользователя который отписываетс
        :return: Объект согласно схеме Success или Failure
        """
        result = await session.execute(
            select(cls).options(
                selectinload(cls.followers),
                selectinload(cls.following),
            ),
        )

        to_follow: Optional[Users] = result.scalars().first()
        if to_follow is not None:
            followers_id: List[int] = [user.id for user in to_follow.following]
        else:
            followers_id = []

        if user_to_follow in followers_id:
            await session.execute(delete(Followings).where(
                Followings.user_id == current_user_id,
                Followings.user_to_follow_id == user_to_follow,
            ),
            )
            await session.commit()
        else:
            logger.error("На пользователя с указанным id вы не подписывались")
            raise AppException(
                "Wrong delete follower",
                "На пользователя с указанным id вы не подписывались",
            )

        return Success.parse_obj({"result": True})

    def to_json(self) -> Dict[str, Any]:
        """
        Метод возвращает словарь.

        :return: возвращает словарь
        """
        return {
            "id": self.id,
            "name": self.username,
            "api_token": self.api_token,
            "followers": [
                {"id": user.id, "name": user.username}
                for user in self.followers
            ],
            "following": [
                {"id": user.id, "name": user.username}
                for user in self.following
            ],
        }


class Tweets(Base):
    __tablename__ = "tweets"
    id: int = Column(Integer, primary_key=True)
    tweet: str = Column(Text(), nullable=False)
    stamp: datetime = Column(DateTime, default=datetime.now)
    user_id: int = Column(Integer, ForeignKey("users.id"), nullable=False)
    user_likes: List["Likes"] = relationship(
        "Likes",
        backref="tweet",
        lazy="selectin",
    )
    images: List["PostImages"] = relationship(
        "PostImages",
        backref="tweet",
        lazy="selectin",
        uselist=True,
    )
    author: Users = relationship(
        "Users",
        backref="tweet",
        lazy="selectin",
    )

    @classmethod
    @error_handler
    async def get_tweets(
            cls,
            session: AsyncSession,
            api_key: str,
    ) -> TweetsOut:
        """
        Метод для получения всех твитов из базы.
        :param session: AsyncSession
        :param api_key: api-key
        :return: Объект согласно схеме TweetsOut или Failure
        """
        query = select(Users).where(Users.api_token == api_key)
        result = await session.execute(query)
        user = result.scalars().first()
        if user is None:
            logger.error("Пользователь с указанным api-key отсутствует в базе")
            raise AppException(
                "api-key not found",
                "Пользователь с указанным api-key отсутствует в базе",
            )

        result = await session.execute(select(cls))
        tweets = result.all()

        lst = []
        for tweet in tweets:
            obj = tweet[0].to_json()
            lst.append(obj)

        return TweetsOut.parse_obj({
            "result": True,
            "tweets": lst,
        })

    @classmethod
    @error_handler
    async def add_new_tweet(
            cls,
            session: AsyncSession,
            tweet: TweetIn,
            user_id: int,
    ) -> NewTweetOut:
        """
        Метод обработки нового твита.

        :param session: AsyncSession
        :param tweet: Информация полученная с фронта согласно схеме TweetIn
        :param user_id: ID пользователя отправившего твит
        :return: Объект согласно схеме TweetSuccess
        """
        new_tweet = Tweets(
            tweet=tweet.tweet_data,
            user_id=user_id,
        )

        session.add(new_tweet)
        await session.flush()
        await session.commit()

        for img_id in tweet.tweet_media_ids:
            postimage = select(PostImages).where(PostImages.image_id == img_id)
            result = await session.execute(postimage)
            post_image: Optional[PostImages] = result.scalars().first()
            if post_image is not None:
                post_image.tweet_id = new_tweet.id
                await session.flush()
                await session.commit()

        return NewTweetOut.parse_obj({
            "result": True,
            "tweet_id": new_tweet.id,
        })

    @classmethod
    @error_handler
    async def add_like(
            cls,
            session: AsyncSession,
            tweet_id: int,
            user_id: int,
    ) -> Success:
        """
        Метод для добавления лайка с твита пользователя.

        :param session: AsyncSession
        :param tweet_id: ID твита на который нужно поставить
        :param user_id: ID пользователя которых хочет поставить
        :return: Объект согласно схеме Success или Failure
        """
        new_like = Likes(tweet_id=tweet_id, user_id=user_id)

        session.add(new_like)
        await session.flush()

        await session.commit()

        return Success.parse_obj({"result": True})

    @classmethod
    @error_handler
    async def delete_like(
            cls,
            session: AsyncSession,
            tweet_id: int,
            user_id: int,
    ) -> Success:
        """
        Метод для удаления лайка с твита пользователя.

        :param session: AsyncSession
        :param tweet_id: ID твита на который нужно поставить/удалить лайк
        :param user_id: ID пользователя которых хочет поставить/удалить лайк
        :return: Объект согласно схеме Success или Failure
        """
        query = delete(Likes).where(
            Likes.user_id == user_id,
            Likes.tweet_id == tweet_id,
        )
        await session.execute(query)
        await session.commit()

        return Success.parse_obj({"result": True})

    @classmethod
    @error_handler
    async def delete_tweet(
            cls,
            session: AsyncSession,
            tweet_id: int,
            user_id: int,
    ) -> Success:
        """
        Метод для удаления твита пользователя.

        :param session: AsyncSession
        :param tweet_id: ID твита для удаления
        :param user_id: ID пользователя, который хочет удалить твит
        :return: Объект согласно схеме Success или Failure
        """
        query_select = select(cls).where(cls.id == tweet_id)
        result = await session.execute(query_select)
        tweet: Optional[Tweets] = result.scalars().first()

        if tweet is not None:
            if tweet.author.id == user_id:
                post_image_query = select(PostImages.image_id).where(
                    PostImages.tweet_id == tweet_id,
                )
                post_image_result = await session.execute(post_image_query)
                post_image_delete = post_image_result.all()

                for img_id in post_image_delete:
                    image_delete_query = delete(PostImages).where(
                        PostImages.image_id == img_id[0],
                    )
                    await session.execute(image_delete_query)
                    await session.commit()

                    image_file: Optional[Images] = await session.get(
                        Images,
                        img_id[0],
                    )

                    image_query = delete(Images).where(Images.id == img_id[0])
                    await session.execute(image_query)
                    await session.commit()

                    if image_file is not None:
                        file_path = Path(str(image_file.file_name))
                        file_path.unlink()

                if tweet.user_likes:
                    query = delete(Likes).where(Likes.tweet_id == tweet.id)
                    await session.execute(query)
                    await session.commit()

                if tweet.user_id == user_id:
                    query = delete(cls).where(cls.id == tweet.id)
                    await session.execute(query)
                    await session.commit()

            else:
                logger.error("Пользователь с указанным id не может удалить твит")
                raise AppException(
                    "user not delete tweet",
                    "Пользователь с указанным id не может удалить твит",
                )

        return Success.parse_obj({"result": True})

    def to_json(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "content": self.tweet,
            "author": {
                "id": self.author.id,
                "name": self.author.username,
            },
            "timestamp": self.stamp.isoformat(),
            "attachments": [image.to_json()["url"] for image in self.images],
            "likes": [like.to_json() for like in self.user_likes],
        }


class Likes(Base):
    __tablename__ = "likes"
    tweet_id: int = Column(
        Integer,
        ForeignKey("tweets.id"),
        primary_key=True,
    )
    user_id: int = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        primary_key=True,
    )
    user: Users = relationship("Users", backref="like", lazy="selectin")

    def to_json(self) -> Dict[str, Any]:
        """
        Возвращает словарь.

        :return dict: dict
        """
        return {
            "name": self.user.username,
            "user_id": self.user_id,
        }


class Followings(Base):
    __tablename__ = "followings"
    user_id: int = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
    )
    user_to_follow_id: int = Column(
        Integer,
        ForeignKey("users.id"),
        primary_key=True,
    )


class PostImages(Base):
    __tablename__ = "post_images"
    id: int = Column(Integer, primary_key=True)
    tweet_id: int = Column(Integer, ForeignKey("tweets.id"))
    image_id: int = Column(
        Integer, ForeignKey("images.id"), nullable=False,
    )
    image: "Images" = relationship(
        "Images",
        backref="postimage",
        lazy="selectin",
    )

    @classmethod
    @error_handler
    async def write_file(
            cls,
            session: AsyncSession,
            file: UploadFile,
    ) -> FileSuccess:
        """
        Метод для записи полученного файла.

        :param session: AsyncSession
        :param file: Полученный файл
        :return: Объект согласно схеме Success или Failure
        """
        home = uploaded_file_path
        filename = str(uuid.uuid4())
        file_name_extension = file.filename.split(".")[1]
        file_name = "{0}.{1}".format(filename, file_name_extension)
        file_path = "images/{image_name}".format(image_name=file_name)
        path_absolute = str(Path(home, file_name))
        file_id = await Images.add_img_to_db(session, file_path)
        await session.commit()

        post_img = PostImages(image_id=file_id)
        session.add(post_img)
        await session.commit()

        async with aiofiles.open(path_absolute, mode="wb") as file_image:
            content = await file.read()
            await file_image.write(content)
        return FileSuccess.parse_obj({
            "result": True,
            "media_id": file_id,
        })

    def to_json(self) -> Dict[str, Any]:

        return {"url": self.image.file_name}


class Images(Base):
    __tablename__ = "images"
    id: int = Column(Integer, primary_key=True)
    file_name: str = Column(Text(), nullable=False)

    @classmethod
    async def add_img_to_db(cls, session: AsyncSession, path: str) -> int:
        """
        Записывает в базу путь для сохранения файла.

        :param session: AsyncSession.
        :param path: путь к файлу.
        :return: id.
        """
        new_img = Images(file_name=path)
        session.add(new_img)
        await session.flush()
        return new_img.id
