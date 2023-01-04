import os
from typing import Union
from typing import AsyncGenerator
from dotenv import load_dotenv
from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from jose.jwt import encode

from app.config import settings
from app.crud.user import UserService
from app.db.models import User
from app.utils.logger import get_logger

logger = get_logger("user_current")
api_key_header = APIKeyHeader(name="api-key", auto_error=False)

# load_dotenv()
#
# secret_key = os.getenv("SECRET_KEY")
# algorithm = os.getenv("ALGORITHM")
secret_key = settings.secret_key
algorithm = settings.algorithm



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
        key=secret_key,
        algorithm=algorithm,
    )
    user: Union[User, None] = await service.get_user_by_token(api_token)

    return user