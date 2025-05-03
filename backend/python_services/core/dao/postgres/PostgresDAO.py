from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres import async_session_maker
from core.exception.BaseHTTPException import BaseHTTPException
from core.param_decorator import func_parameter, AsyncCreatingParameterGenerator


class PostgresDAO:
    
    @classmethod
    @func_parameter(name = 'session', type = AsyncSession)
    async def get_session(cls, auto_commit : bool = False, ignore_http_errors : bool = False):
        response_error : BaseHTTPException | None = None
        
        async with cls.__get_correct_session(auto_commit) as session:
            try:
                yield session
            except BaseHTTPException as error:
                response_error = error
                
                if not ignore_http_errors:
                    raise response_error
                
        if response_error:
            raise response_error    
        
        
                
                
    
    
    
    @staticmethod
    def __get_correct_session(auto_commit : bool) -> AsyncSession:
        if not auto_commit:
            return async_session_maker()
    
        return async_session_maker.begin()
    
    