from typing import Union
from fastapi import APIRouter, Depends, File, UploadFile, status

from app.crud.media import MediaService
from app.db.schemas import Failure, FileSuccess
from app.routers.user_current import current_user
from app.utils.errors import AppException, error_handler
from app.utils.logger import get_logger

logger = get_logger("routers.media")

router = APIRouter(
    prefix="/api/medias",
    tags=["Tweets"],
)


@router.post(
    "",
    response_model=Union[FileSuccess, Failure],
    summary="Загружает файл из твита",
    description="Маршрут - позволяет загрузить файл из твита.",
    response_description="Успешный ответ",
    status_code=status.HTTP_201_CREATED,
)
@error_handler
async def get_new_file(
        user: current_user = Depends(),
        service: MediaService = Depends(),
        file: UploadFile = File(),
) -> Union[FileSuccess, Failure]:
    """
    Endpoint получения файла из твита пользователя.

    :param user:
    :param service:
    :param file: Переданный файл
    :return:  Возвращает объект согласно схеме FileSuccess или Failure
    """
    logger.info("Сохранение файла из твита пользователя.")
    if user is None:
        AppException(
            "api-key not found",
            "Пользовател с таким api-key отстутствует в базе",
        )

    file_id = await service.write_file(file)

    return FileSuccess.parse_obj({
        "result": True,
        "media_id": file_id,
    })
