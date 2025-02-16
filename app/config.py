import os
from pathlib import Path
from typing import Optional

from pydantic import ConfigDict, computed_field
from pydantic_settings import BaseSettings


class Config(BaseSettings):
    model_config = ConfigDict(extra="ignore")

    ENV: Optional[str] = "development"
    DEBUG: Optional[bool] = True
    APP_HOST: Optional[str] = "0.0.0.0"
    APP_PORT: Optional[int] = 8000

    DB_SERVER: str
    DB_PORT: int
    DB_USER: str
    DB_PASSWORD: str
    DB_NAME: str

    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 6379

    @computed_field
    @property
    def SQLALCHEMY_DATABASE_URI(self) -> str:
        return "postgresql+asyncpg://{}:{}@{}:{}/{}".format(
            self.DB_USER, self.DB_PASSWORD, self.DB_SERVER, self.DB_PORT, self.DB_NAME
        )

    SECRET_KEY: Optional[str] = "fastapi"
    JWT_ALGORITHM: Optional[str] = "HS256"


config = Config(_env_file=os.path.join(Path(__file__).parents[1], ".env"))
