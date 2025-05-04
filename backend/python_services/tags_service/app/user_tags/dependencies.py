from functools import lru_cache
from .dao import UserTagsDAO


@lru_cache
def get_user_tags_dao() -> UserTagsDAO:
    return UserTagsDAO()
