from .dao import NewUserDAO
from functools import lru_cache
from .utils import UserTagsNotifyUtils
from fastapi import Depends


@lru_cache
def get_new_user_dao() -> NewUserDAO:
    return NewUserDAO()


@lru_cache
def get_tags_notify_utils(new_user_dao: NewUserDAO = Depends(get_new_user_dao)) -> UserTagsNotifyUtils:
    from core.models.rabbitmq.tags import tags_publisher

    return UserTagsNotifyUtils(tags_publisher, new_user_dao)
