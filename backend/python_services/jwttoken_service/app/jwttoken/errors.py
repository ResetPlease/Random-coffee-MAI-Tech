from core.exception.BaseHTTPException import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import Field, ConfigDict
from enum import StrEnum, auto
from fastapi import status




class IssueErrorType(StrEnum):
    SECRET_KEY_IS_NOT_SPECIFIED = auto()
    INCORRECT_SECRET_KEY = auto()
    INCORRECT_USERID = auto()
    
    
    
class IssueExceptionModel(BaseHTTPExceptionModel):
    
    type : IssueErrorType
    
    model_config = ConfigDict(title = 'Authorization error')



class IssueException(BaseHTTPException):
    pass


SecretKeyIsNotSpecifiedError = IssueException(
                                    status_code = status.HTTP_401_UNAUTHORIZED,
                                    detail = IssueExceptionModel(
                                                            type = IssueErrorType.SECRET_KEY_IS_NOT_SPECIFIED,
                                                            message = 'SecretKey header is not set'
                                                        )
                            )


IncorrectSecretKeyError = IssueException(
                                        status_code = status.HTTP_401_UNAUTHORIZED,
                                        detail = IssueExceptionModel(
                                                                    type = IssueErrorType.INCORRECT_SECRET_KEY,
                                                                    message = 'The seret key is incorrect'
                                                                )
                                    )

IncorrectUserIDError = IssueException(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = IssueExceptionModel(
                                                                    type = IssueErrorType.INCORRECT_USERID,
                                                                    message = 'This id is incorrect'
                                                                )
                                    )