import shutil

from pathlib import Path
from typing import IO, Generator
from uuid import uuid4
import aiofiles
from fastapi import UploadFile, BackgroundTasks, HTTPException
from starlette.requests import Request
from models import User, Image


def allowed_file(filename):
    """
    Функция проверки расширения файла
    :param filename:
    :return: [False, True]
    """
    allowed_extensions = ["txt", "pdf", "png", "jpg", "jpeg", "gif"]
    if '.' in filename and filename.rsplit('.', 1)[1] in allowed_extensions:
        return True
    return False




async def add_image(session, filename, image_data):
    new_image = Image(img_filename=filename,
                      img_data=image_data)
    await session.add(new_image)
    await session.commit()
    return new_image.id