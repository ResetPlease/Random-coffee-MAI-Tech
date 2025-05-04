from .utils import AuthServiceUtils
from functools import lru_cache
from core.dao.http import HTTPRequest


@lru_cache
def get_jwttoken_utils() -> AuthServiceUtils:
    from core.services.auth import auth_service_settings
    
    return AuthServiceUtils(
                                HTTPRequest(),
                                auth_service_settings.NAME,
                                auth_service_settings.PORT,
                                auth_service_settings.VERIFY_TOKENS_ENDPOINT,
                                auth_service_settings.VERIFY_TOKENS_ENDPOINT_METHOD
                            )