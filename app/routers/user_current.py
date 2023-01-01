from typing import Union
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from jose.jwt import encode

from crud.user import UserService
from db.models import User
from settings import settings
from utils.logger import get_logger

logger = get_logger("user_current")
api_key_header = APIKeyHeader(name="api-key", auto_error=False)


async def current_user(
        api_key: str = Depends(api_key_header),
        service: UserService = Depends(),
) -> Union[User, None]:
    """
    Функция возвращает api-key.

    :param api_key: любое слово или сочетание слов.
    :param service:
    :return: пользователь.
    """
    api_token = encode(
        claims={"api-key": api_key},
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )
    user: Union[User, None] = await service.get_user_by_token(api_token)

    return user
