from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import Field, field_validator
from os.path import abspath, dirname
from typing import Any


class CelerySettings(BaseSettings):
    BROKER : str
    BROKER_HOST : str
    BROKER_PORT : int
    BROKER_PASSWORD : str
    BROKER_DB : int = Field(default = 0)
    BACKEND_HOST : str
    BACKEND_PORT : int
    BACKEND_PASSWORD : str
    BACKEND_DB : int = Field(default = 0)
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )


settings = CelerySettings()

def get_broker_url() -> str:
    return f'{settings.BROKER}://:{settings.BROKER_PASSWORD}@{settings.BROKER_HOST}:{settings.BROKER_PORT}/{settings.BROKER_DB}'

def get_backend_url() -> str:
    return f'{settings.BROKER}://:{settings.BACKEND_PASSWORD}@{settings.BACKEND_HOST}:{settings.BACKEND_PORT}/{settings.BACKEND_DB}'

