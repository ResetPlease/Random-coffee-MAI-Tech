from pydantic import PositiveInt






class UpdateUsersUtils:
    
    __slots__ = ('nack_message_block_seconds', )
    
    
    def __init__(self, nack_message_block_seconds : PositiveInt) -> None:
        self.nack_message_block_seconds = nack_message_block_seconds
        