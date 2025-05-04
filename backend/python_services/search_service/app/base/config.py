from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import NonNegativeInt, PositiveInt
from datetime import timedelta


class InitMongoSettings(BaseSettings):
    NEED_INIT : bool
    PAGE_SIZE : PositiveInt
    NACK_MESSAGE_BLOCK_SECONDS: PositiveInt
    MEETING_CLEAR_TIMEDELATA : timedelta
    
    model_config = SettingsConfigDict(
        env_prefix = 'SEARCH_SERVICE_',
        extra = 'ignore',
        frozen = True
    )


search_service_settings = InitMongoSettings()