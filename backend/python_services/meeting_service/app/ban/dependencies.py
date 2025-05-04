from .dao import UserBanListDAO
from functools import lru_cache




@lru_cache
def get_user_banlist_dao() -> UserBanListDAO:
    return UserBanListDAO()