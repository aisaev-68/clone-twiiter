from pathlib import Path

from pydantic import BaseSettings


class Settings(BaseSettings):
    db_user: str
    db_password: str
    db_name: str
    db_host: str
    db_port: int
    algorithm: str
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

    @property
    def database_url(self) -> str:
        """
        Assemble Database URL from settings.
        :return: Database URL.
        """

        return f"postgresql+asyncpg://{self.db_user}:{self.db_password}@{self.db_host}:{self.db_port}/{self.db_name}"


settings = Settings()
uploaded_file_path = Path(__file__).parent / "images"
uploaded_file_path.mkdir(exist_ok=True, parents=True)
uploaded_file_path = uploaded_file_path.absolute()

# DATABASE_URL = "postgresql+asyncpg://{0}:{1}@{2}:{3}/{4}".format(
#     settings.db_user,
#     settings.db_password,
#     settings.db_host,
#     settings.db_port,
#     settings.db_name,
# )
