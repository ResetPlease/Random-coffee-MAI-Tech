from redis.asyncio.client import Pipeline, Redis
from core.models.redis import client
from core.param_decorator import func_parameter, AsyncCreatingParameterGenerator



class RedisDAO: 
    
    @classmethod
    @func_parameter(name = 'pipeline')
    async def get_pipeline(cls) -> AsyncCreatingParameterGenerator[Pipeline]:
        async with client.pipeline() as pipeline:
            yield pipeline
            
    
    @classmethod
    @func_parameter()
    async def get_client(cls) -> AsyncCreatingParameterGenerator[Redis]:
        yield client
    
     
    
    @classmethod
    async def shutdown(cls) -> None:
        await client.aclose()

    
    
    
    
    

