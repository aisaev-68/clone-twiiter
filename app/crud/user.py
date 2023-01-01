from typing import Any, Dict, List, Optional, Union

from fastapi import Depends
from sqlalchemy import delete, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from db.database import get_db
from db.models import Follows, User
from db.schemas import Success, UserOut
from utils.logger import get_logger

logger = get_logger("crud.user")


class UserService:
    """Сервис обработки Endpoint связанных с пользователями."""

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

    async def get_user_info(self, user_id: int) -> Union[User, None]:
        """
        Метод для получения информации о пользователе.

        :param user_id: ID пользователя для получения информации.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(User).where(User.id == user_id).options(
            selectinload(User.followers),
            selectinload(User.follows),
        )

        result = await self.session.execute(query)
        user = result.scalars().first()

        return user

    async def get_user_by_id(self, user_id: int) -> Union[User, None]:
        """
        Метод - получает информацию о пользователе по его ID.

        :param user_id: ID пользователя.
        :return: Информацию о пользователе в виде словаря
        """
        query = select(User).where(User.id == user_id).options(
            selectinload(User.followers),
            selectinload(User.follows),
        )
        result = await self.session.execute(query)
        user = result.scalars().first()

        return user

    async def get_user_by_token(self, api_key: str) -> Union[User, None]:
        """
        Метод получает информацию о пользователе по его ID.

        :param api_key: api-key.
        :return: Информацию о пользователе в виде словаря
        """
        logger.info("Получение информации о текущем пользователе.")
        query = select(User).where(User.api_token == api_key).options(
            selectinload(User.followers),
            selectinload(User.follows),
        )

        result = await self.session.execute(query)
        user: Union[User, None] = result.scalars().first()

        return user

    async def follow(
            self,
            user_to_follow: int,
            current_user_id: int
    ) -> Success:
        """
        Метод для добавления пользователя в подписки.

        :param user_to_follow: ID пользователя на которого необходимо подписаться
        :param current_user_id: ID пользователя который подписывается
        :return: Объект согласно схеме Success или Failure
        """
        result = await self.session.execute(select(User).where(
            User.id == current_user_id).options(
            selectinload(User.followers), selectinload(User.follows),
        )
        )

        to_follow: Optional[User] = result.scalars().first()
        following_id = [user.id for user in to_follow.followers]
        user = await self.session.execute(
            select(User).where(User.id == user_to_follow)
        )
        user = user.one_or_none()

        if user is not None and user_to_follow not in following_id:
            self.session.add(
                Follows(user_id=current_user_id, follows_user_id=user_to_follow)
            )
            await self.session.flush()
            await self.session.commit()
            return True
        else:
            return False

    async def unfollow(
            self,
            user_un_follow: int,
            current_user_id: int
    ) -> Success:
        """
        Метод для удаления пользователя из подписки.

        :param user_un_follow: ID пользователя от которого необходимо отписаться
        :param current_user_id: ID пользователя который отписываетс
        :return: Объект согласно схеме Success или Failure
        """
        result = await self.session.execute(select(User).where(
            User.id == current_user_id).options(
            selectinload(User.followers), selectinload(User.follows),
        )
        )

        to_follow = result.scalars().first()
        followers_id: List[int] = [user.id for user in to_follow.followers]

        if user_un_follow not in followers_id:
            return False

        await self.session.execute(
            delete(Follows).where(
                Follows.user_id == current_user_id,
                Follows.follows_user_id == user_un_follow)
        )
        await self.session.commit()

        return True
