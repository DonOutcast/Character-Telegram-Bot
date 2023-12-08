from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    bot_token: str = Field(..., alias="BOT_TOKEN")

    class Config:
        env_file = ".env"


settings = Settings()
