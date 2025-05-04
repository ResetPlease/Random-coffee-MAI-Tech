from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PositiveInt
from datetime import timedelta
from app.config import SMTPSettings



class ServiceSettings(BaseSettings):
    FIRST_BLOCK_TIME : timedelta
    SECOND_BLOCK_TIME : timedelta
    THIRD_BLOCK_TIME : timedelta
    BLOCK_LIFETIME : timedelta
    CODE_MAX_FAIL_ATTEMPT_COUNT : PositiveInt
    CODE_LENGTH : PositiveInt
    CODE_LIFETIME : timedelta
    SMTP : SMTPSettings
    CODE_PAGE_SERVER : str
    CODE_PAGE_PORT : int
    CODE_PAGE_ENDPOINT : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        env_prefix = 'VERIFY_EMAIL_',
        env_nested_delimiter = '_',
        frozen = True
    )


settings = ServiceSettings()

