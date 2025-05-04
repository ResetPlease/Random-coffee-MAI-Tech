from core.exception.BaseHTTPException import BaseHTTPException, BaseHTTPExceptionModel
from pydantic import Field, ConfigDict
from enum import StrEnum, auto
from fastapi import status


class AccessErrorType(StrEnum):
    TOKEN_IS_NOT_SPECIFIED = auto()
    INCORRECT_AUTH_HEADER_FORM = auto()
    INCORRECT_TOKEN_TYPE = auto()
    INVALID_TOKEN = auto()
    TOKEN_HAS_EXPIRED = auto()
    TOKEN_OWNER_NOT_FOUND = auto()
    TOKEN_REVOKED = auto()
    


    
    
class JWTExceptionModel(BaseHTTPExceptionModel):
    
    type : AccessErrorType
    
    model_config = ConfigDict(title = 'Authorization error')



class JWTException(BaseHTTPException):
    pass



IsNotSpecifiedError = JWTException(
                                    status_code = status.HTTP_401_UNAUTHORIZED,
                                    detail = JWTExceptionModel(
                                                            type = AccessErrorType.TOKEN_IS_NOT_SPECIFIED,
                                                            message = 'Access-token header is not set'
                                                        )
                            )

IncorrectAuthHeaderFromError = JWTException(
                                            status_code = status.HTTP_401_UNAUTHORIZED,
                                            detail = JWTExceptionModel(
                                                            type = AccessErrorType.INCORRECT_AUTH_HEADER_FORM,
                                                            message = 'Access-token must have the form "Bearer <TOKEN>"'
                                                        )
                                        )


IncorrectTokenTypeError = JWTException(
                                        status_code = status.HTTP_401_UNAUTHORIZED,
                                        detail = JWTExceptionModel(
                                                                    type = AccessErrorType.INCORRECT_TOKEN_TYPE,
                                                                    message = 'The passed token does not match the required type'
                                                                )
                                    )

ClientInvalidTokenError = JWTException(
                                        status_code = status.HTTP_401_UNAUTHORIZED,
                                        detail = JWTExceptionModel(
                                                                    type = AccessErrorType.INVALID_TOKEN,
                                                                    message = 'The transferred token is invalid'
                                                                )
                                    )


ExpiredTokenError = JWTException(
                                    status_code = status.HTTP_401_UNAUTHORIZED,
                                    detail = JWTExceptionModel(
                                                                type = AccessErrorType.TOKEN_HAS_EXPIRED,
                                                                message = 'The token lifetime has expired'
                                                            )
                            )

TokenRevokedError = JWTException(
                                status_code = status.HTTP_401_UNAUTHORIZED,
                                detail = JWTExceptionModel(
                                                           type = AccessErrorType.TOKEN_REVOKED,
                                                           message = 'This token has revoked'
                                                       )
                            )
