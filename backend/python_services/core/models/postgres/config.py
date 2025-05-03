from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings


class PostgresSettings(BaseSettings):
    DB : str
    USER : str
    
    model_config = SettingsConfigDict(
        env_prefix = 'POSTGRES_',
        extra = 'ignore',
        frozen = True
    )

postgres_settings = PostgresSettings()


def get_db_url() -> str:
    return (f'postgresql+asyncpg://{postgres_settings.USER}:{postgres_settings.PASSWORD}@'
            f'{postgres_settings.HOST}:{postgres_settings.PORT}/{postgres_settings.DB}')
    
