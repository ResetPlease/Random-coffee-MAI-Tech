from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class AuthErrorType(StrEnum):
    EMAIL_OCCUPIED = auto()
    INVALID_EMAIL = auto()
    INVALID_PASSWORD = auto()
    INCORRECT_CODE = auto()
    CODE_IS_NOT_SPECIFIED = auto()





class AuthExceptionModel(BaseHTTPExceptionModel):
    
    type : AuthErrorType
 
    model_config = ConfigDict(title = 'Ошибка регистации')




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


IncorrectCodeError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                                type = AuthErrorType.INCORRECT_CODE,
                                                                message = 'This email-code is inccorect'
                                                            )
                                )

EmptyCodeError = AuthException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = AuthExceptionModel(
                                                                type = AuthErrorType.CODE_IS_NOT_SPECIFIED,
                                                                message = 'You need send email-code'
                                                            )
                                )

