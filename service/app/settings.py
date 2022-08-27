from dotenv import load_dotenv
from pydantic import BaseSettings
import os

load_dotenv()


class Settings(BaseSettings):
    app_name: str = "Twitter API"
    version: str = "1.0"
    admin: str = "Aysaev Ramazan"


settings = Settings()


ALGORITHM = os.environ.get('ALGORITHM')
SECRET_KEY = os.environ.get("SECRET_KEY")
TTL_JWT = os.environ.get("TTL_JWT")
DB_DEBUG = os.environ.get("DEBUG")


USER = os.environ['USER']
PASSWORD = os.environ['PASSWORD']
HOST = os.environ['HOST']
PORT = os.environ['PORT']
NAME = os.environ['NAME']