from .errors import EmptyCodeError, IncorrectCodeError
from core.services.email import get_email_service_settings
from core.dao.http import HTTPRequest, HTTPResponseType
from fastapi import status
from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from .schemas import UserVerifyPasswordIn


async def verify_code(user_code : UserVerifyPasswordIn) -> None:
        if user_code.code is None:
            raise EmptyCodeError
        
        email_service_settings = get_email_service_settings()
        response = await HTTPRequest.post(   
                                            server = email_service_settings.EMAIL_SERVICE_NAME,
                                            port = email_service_settings.EMAIL_SERVICE_PORT,
                                            endpoint = email_service_settings.VERIFY_CODE_ENDPOINT,
                                            body = {'email' : user_code.email, 'code' : user_code.code},
                                            response_method = HTTPResponseType.JSON
                                        )
        
        if response.get('detail') is not None:
            raise BaseHTTPException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = BaseHTTPExceptionModel.model_validate(response['detail'])
                                )
        
        if response['is_correct_code'] is False:
            raise IncorrectCodeError