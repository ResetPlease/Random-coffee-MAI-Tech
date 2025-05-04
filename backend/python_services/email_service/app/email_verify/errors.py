from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPExceptionModel, LimitException, LimitExceptionModel



class EmailVerifyErrorType(StrEnum):
    EMAIL_BLOCKED = auto()
    MAX_ATTEMPTS  = auto()
    UNKNOWN_EMAIL = auto()
    INCORRECT_OPERATION_ID = auto()



class EmailVerifyExceptionModel(BaseHTTPExceptionModel):
    
    type : EmailVerifyErrorType
    
    model_config = ConfigDict(title = 'Mail validation error')
    
 
    
class EmailVerifyExceptionWithBlockTimeModel(LimitExceptionModel):
    
    type : EmailVerifyErrorType
    
    model_config = ConfigDict(title = 'Mail validation error')




class EmailVerifyException(LimitException):
    pass




EmailBlockedError = EmailVerifyException(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            detail = EmailVerifyExceptionWithBlockTimeModel(
                                            type = EmailVerifyErrorType.EMAIL_BLOCKED,
                                            message = 'your email blocked'
                                       )
                    )


MaxAttemptsError = EmailVerifyException(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            detail = EmailVerifyExceptionModel(
                                    type = EmailVerifyErrorType.MAX_ATTEMPTS,
                                    message = 'you have exceeded the maximum number of attempts'
                               )
                    )

IncorrectOperationID = EmailVerifyException(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            detail = EmailVerifyExceptionModel(
                                    type = EmailVerifyErrorType.INCORRECT_OPERATION_ID,
                                    message = 'incorrect operation id for this email'
                               )
                    )


UnknownEmailError = EmailVerifyException(
                            status_code = status.HTTP_400_BAD_REQUEST,
                            detail = EmailVerifyExceptionModel(
                                    type = EmailVerifyErrorType.UNKNOWN_EMAIL,
                                    message = 'No code of your email'
                               )
                    )




    
    