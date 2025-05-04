from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class SearchProfileErrorType(StrEnum):
    INCORRECT_MIN_MATCH_TAGS = auto()





class SearchProfileExceptionModel(BaseHTTPExceptionModel):
    
    type : SearchProfileErrorType
 
    model_config = ConfigDict(title = 'Search error')
    
    



class SearchProfileException(BaseHTTPException):
    pass



IncorrectMinMatchTagsError = SearchProfileException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = SearchProfileExceptionModel(
                                                                type = SearchProfileErrorType.INCORRECT_MIN_MATCH_TAGS,
                                                                message = 'You have fewer added tags than you indicated as the minimum value'
                                                            )
                                )