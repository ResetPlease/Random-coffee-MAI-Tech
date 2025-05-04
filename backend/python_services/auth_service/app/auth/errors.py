from core.exception import BaseHTTPException, BaseHTTPExceptionModel, LimitException, LimitExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class AuthErrorType(StrEnum):
    EMAIL_OCCUPIED = auto()
    INVALID_EMAIL = auto()
    INVALID_PASSWORD = auto()
    ATTEMPT_COUNT_EXCEEDED = auto()
    ACCESS_BLOCKED = auto()
    






class AuthExceptionModel(BaseHTTPExceptionModel):
    
    type : AuthErrorType
 
    model_config = ConfigDict(title = 'Authtorization error')
    
    

class AuthLimitExceptionModel(LimitExceptionModel):
    type : AuthErrorType
 
    model_config = ConfigDict(title = 'Authtorization error')
    




class AuthException(BaseHTTPException):
    pass




EmailOccupiedError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                                type = AuthErrorType.EMAIL_OCCUPIED,
                                                                message = 'This email is already occupied'
                                                            )
                                )


InvalidEmailError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                               type = AuthErrorType.INVALID_EMAIL,
                                                               message = 'This email not registrate'
                                                           )
                                )

InvalidPasswordError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                                type = AuthErrorType.INVALID_PASSWORD,
                                                                message = 'This password is inccorect'
                                                            )
                                )


AccessBlockedError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                                type = AuthErrorType.ACCESS_BLOCKED,
                                                                message = 'you need to pass verification in one of the ways'
                                                            )
                                )





MaxAttemptsEnterPasswordError = LimitException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthLimitExceptionModel(
                                                                type = AuthErrorType.ATTEMPT_COUNT_EXCEEDED,
                                                                message = 'the number of password entered has been exceeded'
                                                            )
                                )

