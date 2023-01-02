import os
from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str = os.getenv("DB_USER", "")
    db_password: str = os.getenv("DB_PASSWORD", "")
    db_name: str = os.getenv("DB_NAME", "")
    db_host: str = os.getenv("DB_HOST", "")
    asyncpg_url: str = f"postgresql+asyncpg://{db_user}:{db_password}@{db_host}:5432/{db_name}"
    algorithm: str = os.getenv("ALGORITHM", "")
    secret_key: str = os.getenv("SECRET_KEY", "")



settings = Settings()
uploaded_file_path = Path(__file__).parent / "images"
uploaded_file_path.mkdir(exist_ok=True, parents=True)
uploaded_file_path = uploaded_file_path.absolute()
