from pydantic import ConfigDict, PositiveInt, Field
from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from typing import Any



class LimitExceptionModel(BaseHTTPExceptionModel):
    
    remaining_seconds : PositiveInt = Field(default = 0, description = 'seconds before unlock')
    
    model_config = ConfigDict(title = 'Limit request error model')




class LimitException(BaseHTTPException):
    
    
    def set_remaining_seconds(self, seconds : int) -> None:
        if not isinstance(self.detail, LimitExceptionModel):
            raise TypeError('detail not inheritance from LimitExceptionModel')
        self.detail.remaining_seconds = max(self.detail.remaining_seconds, seconds, 0)
            



