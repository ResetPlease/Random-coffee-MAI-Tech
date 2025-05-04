from core.dao.redis import RedisDAO, Redis
from core.schemas import UserID
from core.param_decorator import class_parameter


class NewUserDAO(RedisDAO):

    @staticmethod
    def get_new_user_storage() -> str:
        return 'new_user_storage'

    @class_parameter()
    @RedisDAO.get_client()
    async def is_new_user(cls, client: Redis, user_id: UserID) -> bool:
        return await client.sismember(cls.get_new_user_storage(), user_id)

    @class_parameter()
    @RedisDAO.get_client()
    async def add_new_user(cls, client: Redis, user_id: UserID) -> None:
        await client.sadd(cls.get_new_user_storage(), user_id)

    @class_parameter()
    @RedisDAO.get_client()
    async def remove_new_user(cls, client: Redis, user_id: UserID) -> None:
        await client.srem(cls.get_new_user_storage(), user_id)
