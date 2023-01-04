from pathlib import Path
from pydantic import BaseSettings

class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    algorithm: str
    secret_key: str

    class Config:
        env_file = "../.env"
        env_file_encoding = "utf-8"

settings = Settings()

# uploaded_file_path = Path(__file__).parent / "images"
# uploaded_file_path.mkdir(exist_ok=True, parents=True)
# uploaded_file_path = uploaded_file_path.absolute()

# asyncpg_url: str = f"postgresql+asyncpg://{settings.db_user}:" \
#                    f"{settings.db_password}@" \
#                    f"{settings.db_host}:5432/{settings.db_name}"
