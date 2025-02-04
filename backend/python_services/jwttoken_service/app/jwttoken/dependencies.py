from fastapi import Security
from fastapi.security import APIKeyHeader
from core.services.jwttoken import encoded_secret_key
from .errors import SecretKeyIsNotSpecifiedError, IncorrectSecretKeyError



def check_secret_key(secret_key : str | None = Security(APIKeyHeader(name = 'SecretKey', auto_error = False))) -> str:
    if secret_key is None:
        raise SecretKeyIsNotSpecifiedError
    
    if encoded_secret_key() != secret_key:
        raise IncorrectSecretKeyError
    
    return secret_key
    
    