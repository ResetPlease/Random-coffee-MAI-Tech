from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings
from pydantic import Field


class RedisSettings(BaseSettings):
    DB : int = Field(default = 0)
    
    model_config = SettingsConfigDict(
        env_prefix = 'REDIS_',
        extra = 'ignore',
        frozen = True
    )


redis_settings = RedisSettings()