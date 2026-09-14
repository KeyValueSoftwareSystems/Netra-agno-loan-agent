from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field


class Environment(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

    ENVIRONMENT: str = "dev"
    OPENAI_API_KEY: str = Field()
    DATABASE_PATH: str = Field(default="data/nova.db")


env = Environment()  # type: ignore
