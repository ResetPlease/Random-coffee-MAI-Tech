from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPExceptionModel, BaseHTTPException



class MeetingErrorType(StrEnum):
    INCORRECT_MEETING_DATETIME = auto()
    INCORRECT_USER_ID = auto()
    USER_HAS_MEETING_AT_THIS_TIME = auto()
    CANCELLED_DENIED = auto()
    COMPLETED_DENIED = auto()
    INCORRECT_MEMBER = auto()
    
    



class MeetingExceptionModel(BaseHTTPExceptionModel):
    
    type : MeetingErrorType
    
    model_config = ConfigDict(title = 'Planned neeting error')
    
    
    
class MeetingExeption(BaseHTTPException):
    pass


IncorrectMeetingDatetimeError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.INCORRECT_MEETING_DATETIME,
                                                                        message = 'Check the correctness of the date of the meeting'
                                                                    )
                                    )

IncorrectUserIDError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.INCORRECT_USER_ID,
                                                                        message = 'this user id is not exist'
                                                                    )
                                    )

UserAlreadyHasMettingError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.USER_HAS_MEETING_AT_THIS_TIME,
                                                                        message = 'оne of the members of the meeting has already planned a meeting at that time'
                                                                    )
                                    )



CanceledMeetingError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.CANCELLED_DENIED,
                                                                        message = 'this meeting cannot be canceled'
                                                                    )
                                    )

CompletedMeetingError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.COMPLETED_DENIED,
                                                                        message = 'this meeting cannot be completed'
                                                                    )
                                    )

MemberMeetingError = MeetingExeption(
                                        status_code = status.HTTP_400_BAD_REQUEST,
                                        detail = MeetingExceptionModel(
                                                                        type = MeetingErrorType.INCORRECT_MEMBER,
                                                                        message = 'You are not a member in this meeting'
                                                                    )
                                    )
