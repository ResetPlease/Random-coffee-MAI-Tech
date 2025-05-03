from core.dao.redis import RedisDAO, Redis, Pipeline
from core.param_decorator import self_parameter
from pydantic import PositiveInt, EmailStr
from .errors import MaxAttemptsError, UnknownEmailError, IncorrectOperationID
from uuid import UUID



class VerifyingUserDAO(RedisDAO):
    
    __slots__ = ('code_lifetime', 'max_fail_attempt')
    
    
    def __init__(self, code_lifetime : PositiveInt, max_fail_attempt : PositiveInt) -> None:
        self.code_lifetime = code_lifetime
        self.max_fail_attempt = max_fail_attempt
    
    
    @staticmethod
    def _get_key(email : EmailStr) -> str:
        return f'code:{email}'
    
    
    @staticmethod
    def _get_code_key() -> str:
        return 'code'
    
    
    @staticmethod
    def _get_attempt_count_key() -> str:
        return 'attempt_count'
    
    @staticmethod
    def _get_op_id_key() -> str:
        return 'op_id'
    
    
    
    
    @self_parameter()
    @RedisDAO.get_pipeline()
    async def save_code(    
                        self, 
                        pipeline : Pipeline, 
                        email : EmailStr,
                        code : PositiveInt, 
                        operation_id : UUID
                    ) -> None:
        pipeline.multi()
        key = self._get_key(email)
        code_value = {
                    self._get_code_key() : code, 
                    self._get_op_id_key() : str(operation_id),
                    self._get_attempt_count_key() : 0
                }
        pipeline.hmset(key, mapping = code_value)
        pipeline.expire(key, self.code_lifetime)
        await pipeline.execute()
        
    
    
    @self_parameter()
    @RedisDAO.get_client()
    async def delete_code(self, client : Redis, email : EmailStr) -> None:
        await client.delete(self._get_key(email))
        
        
        
    @self_parameter()
    @RedisDAO.get_client()
    async def is_correct_code(
                                self, 
                                client : Redis,
                                email : EmailStr, 
                                code : PositiveInt,
                                operation_id : UUID
                            ) -> bool:
        key = self._get_key(email)
        correct_code_key, attempt_count_key, op_id_key = self._get_code_key(), self._get_attempt_count_key(), self._get_op_id_key()
        correct_code, attempt_count, correct_op_id = await client.hmget(key, correct_code_key, attempt_count_key, op_id_key)
        
        if correct_code is None or attempt_count is None or correct_op_id is None:
            raise UnknownEmailError
        
        if int(attempt_count) >= self.max_fail_attempt:
            raise MaxAttemptsError
        
        if UUID(correct_op_id.decode()) != operation_id:
            raise IncorrectOperationID
        
        if int(correct_code) == code:
            return True
        
        await client.hincrby(key, attempt_count_key)
        return False
        
        
        
        
        
        
        
        
        
        
        
        