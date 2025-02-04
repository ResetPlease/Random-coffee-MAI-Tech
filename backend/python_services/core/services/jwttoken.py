from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache
from hashlib import sha256


class JWTTokenSecretKey(BaseSettings):
    JWTTOKEN_SERVICE_SECRET_KEY : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )



class JWTTokenServiceSettings(BaseSettings):
    JWT_SERVICE_NAME : str
    JWT_SERVICE_PORT : int
    JWT_ISSUE_TOKENS_ENDPOINT : str
    JWT_VERIFY_TOKENS_ENDPOINT : str
    
    model_config = SettingsConfigDict(
        extra = 'ignore',
        frozen = True
    )
    
    
@lru_cache
def get_jwt_service_settings() -> JWTTokenServiceSettings:
    return JWTTokenServiceSettings()


@lru_cache    
def encoded_secret_key() -> str | None:
    secret_key = JWTTokenSecretKey().JWTTOKEN_SERVICE_SECRET_KEY
    if secret_key is None:
        return None
    return sha256(str.encode(secret_key)).hexdigest() 
