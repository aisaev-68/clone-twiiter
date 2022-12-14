from fastapi import Depends
from fastapi.security.api_key import APIKeyHeader
from jose.jwt import encode

from settings import settings

api_key_header = APIKeyHeader(name="api-key", auto_error=False)


def get_apikey_header(api_key: str = Depends(api_key_header)) -> str:
    """
    Функция возвращает api-key.

    :param api_key: любое слово или сочетание слов.
    :return: зашифрованное строка.
    """
    encoded_jwt = encode(
        claims={"api-key": api_key},
        key=settings.secret_key,
        algorithm=settings.algorithm,
    )
    if api_key is None:
        encoded_jwt = encode(
            claims={"api-key": None},
            key=settings.secret_key,
            algorithm=settings.algorithm,
        )

    return encoded_jwt
