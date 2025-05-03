from .utils import LimiterUtils, timedelta_to_int
from .personal_limiter import PersonalLimiter
from pydantic import PositiveInt
from datetime import timedelta
from typing import Any
from core.exception import LimitException
from .limiter_types import IncrbyConditionType, UnblockConditionType
from .personal_block import PersonalBlock
from .dao import BlockDAO



class RequestLimiter:
    
    __slots__ = ('limiter', 'block_dao')
    
    def __init__(
                self, 
                *blocks_time : tuple[PositiveInt | timedelta, PositiveInt],
                block_lifetime : PositiveInt | timedelta
            )-> None:
        self.limiter = LimiterUtils(*blocks_time, lifetime = block_lifetime)
        self.block_dao = BlockDAO(timedelta_to_int(block_lifetime))
    
    
    def __call__(
                        self,
                        *block_filds : Any, 
                        block_error : LimitException | None = None,
                        incrby_condition : IncrbyConditionType = IncrbyConditionType.ALWAYS,
                        unblock_condition : UnblockConditionType = UnblockConditionType.NEVER,
                        incrby_trigger_errors : list[BaseException] | None = None
                    ) -> PersonalLimiter:
        """
        Args:
            block_error-raise this error if user is blocking. To skip the check for the block, you need to indicate block_error=None
            incrby_condition-condition for incrby block_count
            unblock_condition-condition for set block_count=0
            incrby_trigger_errors-if incrby_condition=ERROR you can indicate which errors will incrby block_count

        """
        
        personal_block = PersonalBlock(self.block_dao, block_filds)
        return PersonalLimiter(self.limiter, personal_block, block_error, incrby_condition, unblock_condition, incrby_trigger_errors)
        
