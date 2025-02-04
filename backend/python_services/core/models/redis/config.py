from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field
from os.path import abspath, dirname


class DBSettings(BaseSettings):
    REDIS_PASSWORD : str
    REDIS_PORT : int
    REDIS_HOST : str
    REDIS_DB : int = Field(default = 0)
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )


settings = DBSettings()
