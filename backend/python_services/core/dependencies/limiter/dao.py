from pydantic import PositiveInt
from core.dao.redis import RedisDAO, Pipeline, Redis
from core.param_decorator import self_parameter



class BlockDAO(RedisDAO):
    
    
    __slots__ = ('lifetime', )
    
    def __init__(self, lifetime : PositiveInt) -> None:
        self.lifetime = lifetime
        
    
    @self_parameter()
    @RedisDAO.get_pipeline()
    async def get_block_count(self, pipeline : Pipeline, block_key : str) -> tuple[int, PositiveInt | None]:
        pipeline.multi()
        pipeline.ttl(block_key)
        pipeline.get(block_key)
        block_time, block_count = await pipeline.execute()
            
        return block_time, int(block_count) if block_count is not None else None
        
            

    @self_parameter()    
    @RedisDAO.get_pipeline()
    async def incrby_block_count(self, pipeline : Pipeline, block_key : str) -> None:
        pipeline.multi()
        pipeline.incrby(block_key)
        pipeline.expire(block_key, self.lifetime)
        await pipeline.execute()
    
    
    @self_parameter()
    @RedisDAO.get_client()
    async def unblock(self, client : Redis, block_key : str) -> None:
        await client.delete(block_key)

        
        