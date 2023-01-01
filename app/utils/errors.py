from functools import wraps
from typing import Any, Callable, TypeVar, cast

from fastapi.responses import JSONResponse

from .logger import get_logger

FunVar = TypeVar("FunVar", bound=Callable[..., Any])

logger = get_logger("error")


def AppException(mtype: str, msg: str):
    raise AppExcept(mtype, msg)

class AppExcept(Exception):
    """
    Пользовательский класс исключений.
    """
    def __init__(self, mtype: str, msg: str):
        super(AppExcept, self).__init__()
        self.mtype = mtype
        self.msg = msg

    def __str__(self) -> str:
        return self.msg


async def create_valid_response(ex_type: str, msg: str) -> JSONResponse:
    """
    Функция для создания корректного ответа.

    :param ex_type: Тип ошибки
    :param msg: Текс ошибки
    :return: объект согласно схеме JSONResponse
    """
    response = {
        "result": False,
        "error_type": ex_type,
        "error_message": msg,
    }

    return JSONResponse(
        response,
        status_code=422,
    )


def error_handler(func: FunVar) -> FunVar:
    """
    Декоратор для обработки исключений внутри методов класса.

    :param func:
    :return:
    """

    @wraps(func)
    async def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return await func(*args, **kwargs)
        except AppExcept as ex:
            logger.error(ex.msg)
            return await create_valid_response(ex.mtype, ex.msg)
        except ValueError as ex:
            logger.info(ex.args)

    return cast(FunVar, wrapper)
