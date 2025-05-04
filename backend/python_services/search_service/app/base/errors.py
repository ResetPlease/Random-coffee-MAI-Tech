from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class SearchErrorType(StrEnum):
    INCORRECT_USER_ID = auto()
    

    






class SearchExceptionModel(BaseHTTPExceptionModel):
    
    type : SearchErrorType
 
    model_config = ConfigDict(title = 'Search error')
    
    



class SearchException(BaseHTTPException):
    pass




IncorrectUserIDError = SearchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = SearchExceptionModel(
                                                                type = SearchErrorType.INCORRECT_USER_ID,
                                                                message = 'There is no such user in the search engine'
                                                            )
                                )