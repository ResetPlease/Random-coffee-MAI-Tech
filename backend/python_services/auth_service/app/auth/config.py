from pydantic_settings import BaseSettings, SettingsConfigDict
from datetime import timedelta
from pydantic import PositiveInt




class AuthtorizationSettings(BaseSettings):
    FIRST_BLOCK_TIME : timedelta
    SECOND_BLOCK_TIME : timedelta
    BLOCK_LIFETIME : timedelta
    MAX_PASSWORD_FAIL_ATTEMPT_BEFORE_FIRST_BLOCK : PositiveInt
    MAX_PASSWORD_FAIL_ATTEMPT_BEFORE_SECOND_BLOCK : PositiveInt
    
    model_config = SettingsConfigDict(
        env_prefix = 'AUTH_',
        extra = 'ignore',
        frozen = True
    )
    
auth_settings = AuthtorizationSettings()
