from pydantic_settings import BaseSettings, SettingsConfigDict
from os.path import abspath, dirname


class DBSettings(BaseSettings):
    POSTGRES_HOST : str
    POSTGRES_PORT : int
    POSTGRES_DB : str
    POSTGRES_USER : str
    POSTGRES_PASSWORD : str
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )


settings = DBSettings()


def get_db_url() -> str:
    return (f'postgresql+asyncpg://{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
            f'{settings.POSTGRES_HOST}:{settings.POSTGRES_PORT}/{settings.POSTGRES_DB}')
    
