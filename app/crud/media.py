import uuid
from pathlib import Path

import aiofiles
from db.database import get_db
from db.models import Media
from fastapi import Depends, UploadFile
from settings import settings, uploaded_file_path
from sqlalchemy.ext.asyncio import AsyncSession
from utils.logger import get_logger

logger = get_logger("crud.media")


class MediaService:
    """
    Класс для обработки Endpoint связанных с media файлами
    """

    def __init__(self, session: AsyncSession = Depends(get_db)):
        self.session = session

    async def write_file(
            self,
            file: UploadFile,
    ):
        """
        Метод для записи полученного файла.

        :param file: Полученный файл
        :return: Объект согласно схеме Success или Failure
        """
        home = uploaded_file_path
        filename = str(uuid.uuid4())
        file_name_extension = file.filename.split(".")[1]
        file_name = "{0}.{1}".format(filename, file_name_extension)
        file_path = "images/{image_name}".format(image_name=file_name)
        path_absolute = str(Path(home, file_name))
        add_img = Media(path_file=file_path)
        self.session.add(add_img)

        await self.session.commit()

        async with aiofiles.open(path_absolute, mode="wb") as file_image:
            content = await file.read()
            await file_image.write(content)
        return add_img.id