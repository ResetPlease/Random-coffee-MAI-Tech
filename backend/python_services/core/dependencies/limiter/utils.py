from pydantic import PositiveInt
from datetime import timedelta


class LimiterUtils:
    
    __slots__ = ('blocks_time', 'lifetime')
    
    def __init__(
                self, 
                *blocks_time : tuple[PositiveInt | timedelta, PositiveInt],
                lifetime : PositiveInt | timedelta
            )-> None:
        self.blocks_time : list[tuple[PositiveInt, PositiveInt]] = []
        self.lifetime = lifetime
        
        
        if isinstance(lifetime, timedelta):
            self.lifetime = timedelta_to_int(self.lifetime)
            
        for time, count in blocks_time:
            if isinstance(time, timedelta):
                time = timedelta_to_int(time)
            
            if self.blocks_time:
                count += self.blocks_time[-1][1]
            self.blocks_time.append((time, count))
        
    
    
    def is_blocked(self, key_ttl : int, block_count : PositiveInt | None) -> bool:
        return self.get_remaining_block_time(key_ttl, block_count) > 0
    
    
    def get_time_to_block(self, block_count : PositiveInt | None) -> PositiveInt:
        if block_count is None:
            return 0
        
        for time, count in self.blocks_time:
            if block_count == count:
                return time 
            
        return self.lifetime if (block_count > count) else 0
    
    
    
    def get_next_block_time(self, block_count : PositiveInt | None) -> PositiveInt:
        block_count = block_count + 1 if block_count is not None else 1
        return self.get_time_to_block(block_count)
    
    
    def get_remaining_block_time(self, key_ttl : int, block_count : PositiveInt | None) -> int:
        if key_ttl < 0 or block_count is None:
            return 0
        
        key_time_live = self.lifetime - key_ttl
        return max(self.get_time_to_block(block_count) - key_time_live, 0)
    
    
    
    def was_there_at_least_one_block(self, block_count : PositiveInt | None) -> bool:
        return block_count is not None and block_count >= self.blocks_time[0][1]
 
        
     
        
def timedelta_to_int(time : timedelta) -> int:
    return int(time.total_seconds())  