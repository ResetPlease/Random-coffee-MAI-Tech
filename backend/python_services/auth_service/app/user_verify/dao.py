from core.dao.redis import RedisDAO, Redis, Pipeline
from pydantic import EmailStr
from uuid import UUID
from datetime import timedelta
from core.param_decorator import self_parameter, class_parameter


class UserVerifyingDAO(RedisDAO):
    
    
    def __init__(self, lifetime : timedelta) -> None:
        self.lifetime = int(lifetime.total_seconds())
        
        
    
    @staticmethod
    def _get_verifying_key(email : EmailStr, op_id : UUID) -> str:
        return f'verify:{email}:{op_id}'
    
    
    @RedisDAO.get_client()
    @self_parameter()
    async def save_user_verification(self, client : Redis, email : EmailStr, op_id : UUID) -> None:
        verifying_key = self._get_verifying_key(email, op_id)
        await client.set(verifying_key, 0, self.lifetime)
        
        
    @class_parameter()
    @RedisDAO.get_client()
    async def delete_user_verification(cls, client : Redis, email : EmailStr, op_id : UUID) -> bool:
        is_exist = await client.delete(cls._get_verifying_key(email, op_id))
        return bool(is_exist)
    
    