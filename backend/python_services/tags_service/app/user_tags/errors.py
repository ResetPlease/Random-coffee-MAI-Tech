from pydantic import ConfigDict
from enum import StrEnum, auto
from fastapi import status
from core.exception import BaseHTTPExceptionModel, BaseHTTPException


class UserTagsErrorType(StrEnum):
    INCORRECT_TAG_ID = auto()


class UserTagsExceptionModel(BaseHTTPExceptionModel):

    type: UserTagsErrorType

    model_config = ConfigDict(title='User tags action error')


class UserTagsExeption(BaseHTTPException):
    pass


IncorrectTagIDError = UserTagsExeption(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = UserTagsExceptionModel(
                                        type = UserTagsErrorType.INCORRECT_TAG_ID,
                                        message = 'Tag with such ID does not exist',
                                    ),
                                )
