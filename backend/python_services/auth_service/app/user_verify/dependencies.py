from .dao import UserVerifyingDAO
from functools import lru_cache





@lru_cache
def get_user_verifying_dao() -> UserVerifyingDAO:
    from .config import verification_settings
    return UserVerifyingDAO(verification_settings.LIFETIME)