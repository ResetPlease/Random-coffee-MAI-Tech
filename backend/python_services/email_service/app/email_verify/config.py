from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PositiveInt, Field
from os.path import abspath, dirname


class ServiceSettings(BaseSettings):
    FIRST_BLOCK_TIME : PositiveInt
    SECOND_BLOCK_TIME : PositiveInt
    THIRD_BLOCK_TIME : PositiveInt
    CODE_MAX_FAIL_ATTEMPT_COUNT : PositiveInt
    KEY_AFTER_UNBLOCK_LIFETIME : PositiveInt
    CODE_LENGTH : PositiveInt
    CODE_LIFETIME : PositiveInt
    SMTP_SERVER : str
    SMTP_PORT : PositiveInt
    VERIFY_EMAIL_LOGIN : str
    VERIFY_EMAIL_PASSWORD : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )


settings = ServiceSettings()
