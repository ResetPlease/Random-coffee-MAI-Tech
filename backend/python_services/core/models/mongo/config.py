from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings


class MongoSettings(BaseSettings):
    USER : str
    
    model_config = SettingsConfigDict(
        env_prefix = 'MONGO_',
        extra = 'ignore',
        frozen = True
    )

mongo_settings = MongoSettings()

def get_url() -> str:
    return (f'mongodb://{mongo_settings.USER}:{mongo_settings.PASSWORD}@{mongo_settings.HOST}:{mongo_settings.PORT}/')