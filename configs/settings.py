from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        case_sensitive=False, env_file=".env", env_file_encoding="utf-8"
    )
    log_path = Field(
        Path(__file__).parent.parent.joinpath("logs").joinpath("app.log")
    )


settings = Settings()
