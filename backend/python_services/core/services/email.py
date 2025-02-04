from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache


class EmailServiceSettings(BaseSettings):
    EMAIL_SERVICE_NAME : str
    EMAIL_SERVICE_PORT : int
    VERIFY_CODE_ENDPOINT : str
    
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )
    
    
@lru_cache
def get_email_service_settings() -> EmailServiceSettings:
    return EmailServiceSettings()
