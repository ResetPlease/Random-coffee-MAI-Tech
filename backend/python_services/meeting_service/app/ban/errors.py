from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPExceptionModel, BaseHTTPException



class UserBanErrorType(StrEnum):
    INCORRECT_USER_ID = auto()
    YOURSELF_BANNED = auto()
    



class UserBanExceptionModel(BaseHTTPExceptionModel):
    
    type : UserBanErrorType
    
    model_config = ConfigDict(title = 'Planned neeting error')
    
    
    
class UserBanExeption(BaseHTTPException):
    pass



IncorrectUserIDError = UserBanExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = UserBanExceptionModel(
                                                                        type = UserBanErrorType.INCORRECT_USER_ID,
                                                                        message = 'this user Id is incorrect'
                                                                    )
                                    )


YourselfBannedError = UserBanExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = UserBanExceptionModel(
                                                                        type = UserBanErrorType.YOURSELF_BANNED,
                                                                        message = 'you cannot ban yourself'
                                                                    )
                                    )