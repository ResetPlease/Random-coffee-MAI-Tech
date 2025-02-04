from sqlalchemy.ext.asyncio import AsyncSession
from core.models.postgres import async_session_maker
from core.exception.BaseHTTPException import BaseHTTPException
from typing import Any



class PostgresDAO:
    
    
    
    @staticmethod
    def __get_correct_session(auto_commit : bool) -> AsyncSession:
        if not auto_commit:
            return async_session_maker()
    
        return async_session_maker.begin()
    
    @classmethod
    def __find_session_in_args_kw(cls, *args, **kwargs) -> tuple[AsyncSession, tuple[Any], dict[str, Any]]:
        if kwargs.get('session') is not None:
            return kwargs.pop('session'), args, kwargs
        
        for index, item in enumerate(args):
            if isinstance(item, AsyncSession):
                return item, args[:index] + args[index + 1:], kwargs
        
        return None, args, kwargs

    
    @classmethod
    def get_session(cls, auto_commit : bool = False, ignore_http_errors : bool = False):
        
        def decorator(func):
            
            async def wrapper(*args, **kwargs):
                responce_error : BaseHTTPException | None = None
                sess, args, kwargs = cls.__find_session_in_args_kw(*args, **kwargs)
                
                if sess is not None:
                    return await func(*args, session = session, **kwargs)
                
                async with cls.__get_correct_session(auto_commit) as session:
                    try:
                        return await func(*args, session = session, **kwargs)
                    except BaseHTTPException as error:
                        responce_error = error

                    if not ignore_http_errors:
                        raise responce_error
                
                raise responce_error
                
                  
            return wrapper
        return decorator