from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")
    amplitude_api_key: str = Field(..., alias="AMPLITUDE_API_KEY")
    amplitude_url: str = Field(..., alias="AMPLITUDE_URL")
    postgres_user: str = Field(..., alias="POSTGRES_USER")
    postgres_password: str = Field(..., alias="POSTGRES_PASSWORD")
    postgres_host: str = Field(..., alias="POSTGRES_HOST")
    postgres_port: str = Field(..., alias="POSTGRES_PORT")
    postgres_db: str = Field(..., alias="POSTGRES_DB")

    class Config:
        env_file = ".env"

    @property
    def get_postgresql_url(self):
        return f"postgresql+asyncpg://{self.postgres_user}:{self.postgres_password}@{self.postgres_host}:"\
               f"{self.postgres_port}/{self.postgres_db}"


BASE_DIR = Path(__file__).parent
TEMPLATE_DIR = BASE_DIR / "templates"

settings = Settings()
