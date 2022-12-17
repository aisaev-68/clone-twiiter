from fastapi import APIRouter, Depends, File, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from db.database import get_db
from utils.get_token_header import get_apikey_header
from utils.logger import get_logger
from db.models import PostImages, Users
from db.schemas import FileSuccess
from utils.errors import AppException

logger = get_logger("routers.medias")

router = APIRouter(
    prefix="/api/medias",
    tags=["Tweets"],
)


@router.post(
    "",
    response_model=FileSuccess,
    summary="Загружает файл из твита",
    description="Маршрут - позволяет загрузить файл из твита.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
    )
async def get_new_file(
        api_key: str = Depends(get_apikey_header),
        session: AsyncSession = Depends(get_db),
        file: UploadFile = File(),
) -> FileSuccess:
    """
    Endpoint получения файла из твита пользователя.

    :param api_key:
    :param session: AsyncSession
    :param file: Переданный файл
    :return:  Возвращает объект согласно схеме FileSuccess или Failure
    """
    logger.info("Сохранение файла из твита пользователя.")
    user = (await Users.get_user_by_token(session, api_key)).dict()
    if user is None:
        raise AppException(
            "api-key njt found",
            "Пользовател с таким api-key отстутствует в базе",
        )
    response = await PostImages.write_file(session, file)

    return response
