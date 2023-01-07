import os
from functools import lru_cache
from pathlib import Path
from typing import Any, Dict, Optional, Union

from pydantic import BaseSettings, PostgresDsn, validator


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: Union[int, str]
    algorithm: str
    secret_key: str
    async_db_uri: Optional[str]

    @validator("async_db_uri", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("db_user"),
            password=values.get("db_password"),
            host=values.get("db_host"),
            port=str(values.get("db_port")),
            path=f"/{values.get('db_name')}",
        )

    @staticmethod
    def path_image() -> Path:
        uploaded_file_path = Path(__file__).parent / "images"
        uploaded_file_path.mkdir(exist_ok=True, parents=True)
        uploaded_file_path = uploaded_file_path.absolute()

        return uploaded_file_path

    class Config:
        # case_sensitive = True
        env_file = os.path.join(os.getcwd(), ".env")
        env_file_encoding = "utf-8"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
