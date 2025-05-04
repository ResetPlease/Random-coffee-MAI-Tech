from .dao import UsersSearchDAO
from functools import lru_cache
from .utils import SearchUtils






@lru_cache
def get_users_search_dao() -> UsersSearchDAO:
    return UsersSearchDAO()


@lru_cache
def get_search_utils() -> SearchUtils:
    from app.base.config import search_service_settings
    
    return SearchUtils(search_service_settings.PAGE_SIZE)
    