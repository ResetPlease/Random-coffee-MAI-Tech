from redis.asyncio import Redis
from redis.asyncio.client import Pipeline
from core.models.redis import settings

class RedisDAO:
    
    __client = Redis(host = settings.REDIS_HOST, port = settings.REDIS_PORT, password = settings.REDIS_PASSWORD, db = settings.REDIS_DB)
    
    @classmethod
    def get_pipeline(cls):
        
        def decorator(func):
            
            async def wrapper(*args : tuple, **kwargs):
                if isinstance(args[-1], Pipeline):
                    return await func(*args, **kwargs)
                
                async with cls.__client.pipeline() as pipeline:
                    return await func(*args, pipeline = pipeline, **kwargs)
            
            return wrapper
        
        return decorator
    
    
    @classmethod
    async def shutdown(cls) -> None:
        await cls.__client.aclose()

    
    
    
    
    

