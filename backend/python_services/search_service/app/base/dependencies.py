from .dao import UsersDAO
from functools import lru_cache




@lru_cache
def get_users_dao() -> UsersDAO:
    return UsersDAO()
