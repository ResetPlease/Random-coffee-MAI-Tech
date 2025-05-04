from .utils import LimiterUtils
from typing import Any, Self, Iterable
from types import TracebackType
from .personal_block import PersonalBlock
from .limiter_types import IncrbyConditionType, UnblockConditionType
from core.exception import LimitException





class PersonalLimiter:
    
    
    __slots__ = (
                    'limiter', 
                    'presonal_block',
                    'block_error', 
                    'incrby_condition', 
                    'unblock_condition', 
                    'incrby_trigger_errors'
                )
    
    def __init__(
                self,
                limiter : LimiterUtils,
                presonal_block : PersonalBlock,
                block_error : LimitException | None = None,
                incrby_condition : IncrbyConditionType = IncrbyConditionType.ALWAYS,
                unblock_condition : UnblockConditionType = UnblockConditionType.NEVER,
                incrby_trigger_errors : Iterable[BaseException] | None = None
            ) -> None:
        self.limiter = limiter   
        self.presonal_block = presonal_block
        self.block_error = block_error 
        self.incrby_condition = incrby_condition
        self.unblock_condition = unblock_condition
        self.incrby_trigger_errors = incrby_trigger_errors
        
        
        if self.incrby_trigger_errors and incrby_condition != IncrbyConditionType.ERROR:
            raise AttributeError('incrby_trigger_errors set only when incrby_condition=ERROR')

    
   
    
    def _need_incrby(self, exc_value : Exception | None) -> bool:
        
        return (
                    self.incrby_condition == IncrbyConditionType.ALWAYS
                ) or (
                    self.incrby_condition == IncrbyConditionType.SUCCESS and exc_value is None
                ) or (
                    (
                        self.incrby_condition == IncrbyConditionType.ERROR and exc_value is not None
                    ) and (
                        self.incrby_trigger_errors is None or any((exc_value is trigger_error for trigger_error in self.incrby_trigger_errors))
                    )
                )
                
                
                
    def _need_unblock(self, exc_value : Exception | None) -> None:
        return (
                self.unblock_condition == UnblockConditionType.SUCCESS and exc_value is None
            )
    
    
    async def get_remaining_block_time(self) -> int:
        block_time, block_count = await self.presonal_block.get_block_count()
        return self.limiter.get_remaining_block_time(block_time, block_count)
    
    
    async def get_next_block_time(self) -> int:
        _, block_count = await self.presonal_block.get_block_count()
        return self.limiter.get_next_block_time(block_count)
    
    
        
    async def is_blocked(self) -> bool:
        block_time, block_count = await self.presonal_block.get_block_count()
        return self.limiter.is_blocked(block_time, block_count)
    
    
    async def was_there_at_least_one_block(self) -> bool:
        block_time, block_count = await self.presonal_block.get_block_count()
        return self.limiter.was_there_at_least_one_block(block_time, block_count)
        
        
        
    async def __aenter__(self) -> Self:
        
        if self.block_error is not None and await self.is_blocked():
            new_block_error = self.block_error.copy()
            new_block_error.set_remaining_seconds(await self.get_remaining_block_time())
            raise new_block_error
        
        return self
    

    
    
    async def __aexit__(
                            self, 
                            exc_type : type[Exception] | None,
                            exc_value : Exception | None,
                            traceback : TracebackType | None
                        ) -> None:
        if self._need_unblock(exc_value):
            await self.presonal_block.unblock()
            return
            
        if self._need_incrby(exc_value):
            await self.presonal_block.incrby_block_count()
        
        
    
    
            
        
        
        
        
        
            
        
        
    
    
        
    
        