from typing import Union, List, Any, Dict, Optional

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from sqlalchemy import (
    delete,
    select,
)
from db.schemas import (
    Success,
    UserOut,
)
from utils.logger import get_logger
from utils.errors import AppException, error_handler
from db.models import User, followers
from db.database import get_db

logger = get_logger("crud.user")


class UserService:
    """
    Сервис обработки Endpoint связанных с пользователями
    """

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session
    async def get_all_users(self) -> Union[List[Any], Dict[str, Any]]:
        """
        Метод возвращает всех пользователей из базы.

        :param session: AsyncSession
        :return: список объектов Users
        """
        users = await self.session.execute(select(User))

        return users.scalars().all()


    async def get_user_info(self, user_id: int = None,) -> UserOut:
        """
        Метод для получения информации о пользователе.

        :param session: AsyncSession
        :param user_id: ID пользователя о котором необходимо
        получить информацию.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(User).where(User.id == user_id).options(
            selectinload(User.followed),
        )

        result = await self.session.execute(query)
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


    async def get_user_by_id(self, user_id: int):
        """
        Метод - получает информацию о пользователе по его ID.

        :param session: AsyncSession
        :param user_id: ID пользователя.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(User).where(
            User.id == user_id
        ).options(selectinload(User.followed),
                  )
        result = await self.session.execute(query)
        user = result.scalars().first()

        return user


    async def get_user_by_token(self, api_key: str,):
        """
        Метод получает информацию о пользователе по его ID.

        :param api_key: api-key.
        :return: Информацию о пользователе в виде словаря
        """
        logger.info("Получение информации о текущем пользователе.")
        query = select(User).where(User.api_token == api_key).options(
            selectinload(User.followers),
            selectinload(User.following))
        result = await self.session.execute(query,)
        user: User = result.scalars().first()

        return user


    async def follow(
            self,
            user_to_follow: int,
            current_user_id: int,
    ):
        """
        Метод для добавления пользователя в подписки и удаления из них.

        :param session: AsyncSession
        :param user_to_follow: ID пользователя на которого необходимо подписаться
        :param current_user_id: ID пользователя который подписывается
        :return: Объект согласно схеме Success или Failure
        """
        result = await self.session.execute(
            select(User).options(
                selectinload(User.followed),
            ),
        )

        to_follow: Optional[User] = result.scalars().first()
        if to_follow is not None:
            following_id: List[int] = [user.id for user in to_follow.followed]
        else:
            following_id = []

        if user_to_follow not in following_id:
            self.session.add(
                followers(
                    follower_id=current_user_id,
                    followed_id=user_to_follow,
                ),
            )
            await self.session.flush()
            await self.session.commit()
        else:
            logger.error("Пользователь с указанным id уже подписан")
            raise AppException(
                "Wrong add follower",
                "Пользователь с указанным id уже подписан",
            )

        return Success.parse_obj({"result": True})

    #
    # @error_handler
    # async def unfollow(
    #         self,
    #         user_to_follow: int,
    #         current_user_id: int,
    # ) -> Success:
    #     """
    #     Метод для удаления пользователя из подписки.
    #
    #     :param session: AsyncSession
    #     :param user_to_follow: ID пользователя от которого необходимо отписаться
    #     :param current_user_id: ID пользователя который отписываетс
    #     :return: Объект согласно схеме Success или Failure
    #     """
    #     result = await self.session.execute(
    #         select(User).options(
    #             selectinload(User.followed),
    #         ),
    #     )
    #
    #     to_follow: Optional[User] = result.scalars().first()
    #     if to_follow is not None:
    #         followers_id: List[int] = [user.id for user in to_follow.followed]
    #     else:
    #         followers_id = []
    #
    #     if user_to_follow in followers_id:
    #         await self.session.execute(delete(followers).where(
    #             followers.follower_id == current_user_id,
    #             followers.followed_id == user_to_follow,
    #         ),
    #         )
    #         await self.session.commit()
    #     else:
    #         logger.error("На пользователя с указанным id вы не подписывались")
    #         raise AppException(
    #             "Wrong delete follower",
    #             "На пользователя с указанным id вы не подписывались",
    #         )
    #
    #     return Success.parse_obj({"result": True})
