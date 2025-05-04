from core.dependencies.JWTToken import TokenRevokedError
from core.schemas import UserID
from core.dao.redis import RedisDAO, Redis, Pipeline
from core.param_decorator import self_parameter, class_parameter
from uuid import UUID
from pydantic import PositiveInt
from datetime import datetime





class JWTTokenStorageDAO(RedisDAO):
    
    
    @staticmethod
    def get_time_now() -> int:
        return int(datetime.now().timestamp())
    
    
    
    @staticmethod
    def _get_tokens_storage_key(user_id : UserID) -> str:
        return f'jwttoken:storage:{user_id}'
    
    
    @staticmethod
    def _get_token_structure(device_id : UUID, exp_at : int) -> dict[str, int]:
        return {str(device_id) : exp_at}
    
     
    @class_parameter()
    @RedisDAO.get_client()
    async def _delete_expire_tokens(cls, client : Redis, storage_key : str) -> None:
        await client.zremrangebyscore(storage_key, 0, cls.get_time_now())
           
    
    
    @class_parameter()
    @RedisDAO.get_pipeline()
    async def save_token_in_storage(
                                    cls,
                                    pipeline : Pipeline, 
                                    user_id : UserID,
                                    device_id : UUID,
                                    token_lifetime : PositiveInt
                                ) -> None:
        storage_key = cls._get_tokens_storage_key(user_id)
        token_exp_at = cls.get_time_now() + token_lifetime
        
        pipeline.multi()
        pipeline.zadd(storage_key, cls._get_token_structure(device_id, token_exp_at))
        pipeline.expireat(storage_key, token_exp_at)
        await pipeline.execute()
        
        await cls._delete_expire_tokens(storage_key)
        
    
    
    @class_parameter()
    @RedisDAO.get_client()
    async def delete_token_from_storage(
                                        cls,
                                        client : Redis, 
                                        user_id : UserID,
                                        device_id : UUID,
                                    ) -> None:
        storage_key = cls._get_tokens_storage_key(user_id)
        await client.zrem(storage_key, str(device_id))
        await cls._delete_expire_tokens(storage_key)
        
    
    
    @class_parameter()
    @RedisDAO.get_client()
    async def get_all_tokens_by_user_id(cls, client : Redis, user_id : UserID) -> list[UUID]:
        tokens : list[bytes] = await client.zrange(cls._get_tokens_storage_key(user_id), 0, -1)
        return [UUID(token.decode()) for token in tokens]
        
    
    
    @class_parameter()
    @RedisDAO.get_client()
    async def delete_storage(cls, client : Redis, user_id : UserID) -> None:
        await client.delete(cls._get_tokens_storage_key(user_id))
    
    
    
    



class JWTTokenDAO(RedisDAO):
    
    
    __slots__ = ('token_lifetime', 'jwt_token_storage_dao')
    
    def __init__(
                    self,
                    token_lifetime : PositiveInt,
                    jwt_token_storage_dao : JWTTokenStorageDAO
                ) -> None:
        self.token_lifetime = token_lifetime
        self.jwt_token_storage_dao = jwt_token_storage_dao
        
        
    
    @staticmethod
    def _get_token_key(user_id : UserID, device_id : UUID) -> str:
        return f'jwttoken:{user_id}:{device_id}'
    
    
    @staticmethod
    def _is_valid_token_version(correct_version : bytes | None, token_version : UUID) -> bool:
        return correct_version is not None and UUID(correct_version.decode()) == token_version
    
    

    @classmethod
    async def _get_token_version(
                                cls, 
                                client : Redis,
                                user_id : UserID,
                                device_id : UUID
                            ) -> bytes | None:
        return await client.get(cls._get_token_key(user_id, device_id))
        
    
    
    @self_parameter()
    @RedisDAO.get_client()
    async def save_token(
                        self, 
                        client : Redis,
                        user_id : UserID,
                        device_id : UUID,
                        version : UUID
                    ) -> None:
        token_key = self._get_token_key(user_id, device_id)
        await client.set(token_key, str(version), self.token_lifetime)
        await self.jwt_token_storage_dao.save_token_in_storage(user_id, device_id, self.token_lifetime)

    
        
    @self_parameter()
    @RedisDAO.get_client()
    async def delete_token( 
                                self, 
                                client : Redis,
                                user_id : UserID,
                                device_id : UUID
                            ) -> None:
        await client.delete(self._get_token_key(user_id, device_id))
        await self.jwt_token_storage_dao.delete_token_from_storage(client, user_id, device_id)
        
        
        
    @self_parameter()
    @RedisDAO.get_client()
    async def delete_all_user_tokens(
                                        self, 
                                        client : Redis,
                                        user_id : UserID,
                                ) -> None:
        tokens_device_ids = await self.jwt_token_storage_dao.get_all_tokens_by_user_id(client, user_id)
        await client.delete(*(self._get_token_key(user_id, device_id) for device_id in tokens_device_ids))
        await self.jwt_token_storage_dao.delete_storage(client, user_id)
        
        
        
        
    @class_parameter()
    @RedisDAO.get_client()
    async def verify_token(
                           cls, 
                           user_id : UserID,
                           device_id : UUID,
                           version : UUID,
                           client : Redis
                       ) -> None:
        correct_token_version = await cls._get_token_version(client, user_id, device_id)
        if not cls._is_valid_token_version(correct_token_version, version):
            raise TokenRevokedError
        
        
        
    @self_parameter()
    @RedisDAO.get_client()
    async def update_token(
                            self, 
                            client : Redis,
                            user_id : UserID,
                            device_id : UUID,
                            old_version : UUID,
                            new_version : UUID
                        ) -> None:
        correct_token_version = await self._get_token_version(client, user_id, device_id)
    
        if not self._is_valid_token_version(correct_token_version, old_version):
            await self.delete_all_user_tokens(client, user_id)
            raise TokenRevokedError
        
        await self.save_token(client, user_id, device_id, new_version)
        
        
