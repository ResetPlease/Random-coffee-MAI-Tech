from pydantic_settings import BaseSettings, SettingsConfigDict
from core.dao.http import HTTPMethod


class AuthServiceSettings(BaseSettings):
    NAME : str
    PORT : int
    VERIFY_TOKENS_ENDPOINT : str
    VERIFY_TOKENS_ENDPOINT_METHOD : HTTPMethod
    
    model_config = SettingsConfigDict(
        env_prefix = 'AUTH_SERVICE_',
        extra = 'ignore',
        frozen = True
    )
    

auth_service_settings = AuthServiceSettings()

