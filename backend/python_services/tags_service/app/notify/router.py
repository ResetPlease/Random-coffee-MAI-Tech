from core.models.rabbitmq.user import get_create_user_subscriber, CreateUserNotify
from core.models.rabbitmq import rabbitmq_router
from .dao import NewUserDAO
from .dependencies import get_new_user_dao
from fastapi import Depends


@get_create_user_subscriber('tags_service.create_user')
async def add_new_user(form: CreateUserNotify, new_user_dao: NewUserDAO = Depends(get_new_user_dao)) -> None:
    await new_user_dao.add_new_user(form.user_id)
