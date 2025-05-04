from .dao import BlockDAO
from typing import Any
from datetime import datetime
from pydantic import PositiveInt
from .utils import timedelta_to_int


class PersonalBlock:
    
    
    __slots__ = (
                    'block_key', 
                    'block_dao',
                    '_block_count_call_time',
                    '_block_time',
                    '_block_count',
                    '_need_update'
                )
    
    
    def __init__(self, block_dao : BlockDAO, block_filds : tuple[Any, ...]) -> None:
        self.block_key = self._get_key(block_filds)
        self.block_dao = block_dao
        self._block_count_call_time : datetime | None = None
        self._block_time : int | None = None
        self._block_count : PositiveInt | None = None
        self._need_update : bool = True
    
    
    @staticmethod
    def _get_key(block_filds : tuple[Any, ...]) -> str:
        return 'block:' + ':'.join(block_filds)
    
      
    async def get_block_count(self, use_cache : bool = True) -> tuple[int, PositiveInt | None]:
        if self._need_update or not use_cache:
            self._block_time, self._block_count = await self.block_dao.get_block_count(self.block_key)
            self._block_count_call_time = datetime.now()
        
        time_has_passed_since_the_last_call = timedelta_to_int(datetime.now() - self._block_count_call_time)
        
        return self._block_time - time_has_passed_since_the_last_call, self._block_count
        
    
    
    async def incrby_block_count(self) -> None:
        await self.block_dao.incrby_block_count(block_key = self.block_key)
        self._need_update : bool = True
       
        
    async def unblock(self) -> None:
        await self.block_dao.unblock(block_key = self.block_key)
        self._need_update : bool = True
        