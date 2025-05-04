from .dao import TagDAO
from functools import lru_cache


@lru_cache
def get_tag_dao() -> TagDAO:
    return TagDAO()
