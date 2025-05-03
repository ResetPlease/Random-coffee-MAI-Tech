from app.base import SearchException, SearchExceptionModel
from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status





class MatchErrorType(StrEnum):
    SAME_USER_ID = auto()
    NOT_ACTIVE_SEARCH_USER = auto()
    USER_IN_BAN_LIST = auto()
    INCORRECT_DATETIME = auto()
    FEW_MATCHING_TAGS = auto()
    





class MatchExceptionModel(SearchExceptionModel):
    
    type : MatchErrorType
 
    model_config = ConfigDict(title = 'Search error')
    
    



class MatchException(SearchException):
    pass




NotActiveUserError = MatchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = MatchExceptionModel(
                                                                type = MatchErrorType.NOT_ACTIVE_SEARCH_USER,
                                                                message = 'This user has no active meetings now'
                                                            )
                                )

UserBannedError = MatchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = MatchExceptionModel(
                                                                type = MatchErrorType.USER_IN_BAN_LIST,
                                                                message = 'You are banned by this user'
                                                            )
                                    )


IncorrectDatetimeError = MatchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = MatchExceptionModel(
                                                                type = MatchErrorType.INCORRECT_DATETIME,
                                                                message = 'This user has no active meetings at this time'
                                                            )
                                )

SameUserIDError = MatchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = MatchExceptionModel(
                                                                type = MatchErrorType.SAME_USER_ID,
                                                                message = 'You cannot start meetings with yourselfу'
                                                            )
                                )


MatchTagsError = MatchException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = MatchExceptionModel(
                                                                type = MatchErrorType.FEW_MATCHING_TAGS,
                                                                message = 'You have few identical tags with this user'
                                                            )
                                )
