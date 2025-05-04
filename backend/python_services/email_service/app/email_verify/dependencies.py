from core.dependencies.limiter import RequestLimiter, PersonalLimiter, IncrbyConditionType
from fastapi import Depends
from .errors import EmailBlockedError
from fastapi import Request
from .schemas import SendEmailIn
from .dao import VerifyingUserDAO
from .utils import EmailVerifyUtils, AuthVerifyUtils
from functools import lru_cache
from typing import AsyncGenerator
from app.base import get_send_simple_email_publisher
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher



        


@lru_cache
def get_code_send_limiter() -> RequestLimiter:
    from .config import settings
    
    return RequestLimiter(
                        (settings.FIRST_BLOCK_TIME, 1), 
                        (settings.SECOND_BLOCK_TIME, 1),
                        (settings.THIRD_BLOCK_TIME, 1),
                        block_lifetime = settings.BLOCK_LIFETIME
                    )




@lru_cache
def get_email_verify_dao() -> VerifyingUserDAO:
    from .config import settings
    
    return VerifyingUserDAO(settings.CODE_LIFETIME, settings.CODE_MAX_FAIL_ATTEMPT_COUNT)
    


@lru_cache
def get_email_verify_utils(publisher : AsyncAPIPublisher = Depends(get_send_simple_email_publisher)) -> EmailVerifyUtils:
    from .config import settings
    
    return EmailVerifyUtils(
                            publisher,
                            settings.CODE_LENGTH,
                            settings.SMTP,
                            settings.CODE_PAGE_SERVER,
                            settings.CODE_PAGE_PORT,
                            settings.CODE_PAGE_ENDPOINT
                        )
    
    
    
@lru_cache
def get_auth_verify_utils() -> AuthVerifyUtils:
    from core.models.rabbitmq.auth import auth_verify_publisher
    
    return AuthVerifyUtils(auth_verify_publisher)



async def get_code_send_limit(
                            request : Request,
                            form : SendEmailIn, 
                            code_send_limiter : RequestLimiter = Depends(get_code_send_limiter)
                        ) -> AsyncGenerator[PersonalLimiter, None]:
    
    async with code_send_limiter(
                                request.url.path,
                                form.email,
                                block_error = EmailBlockedError,
                                incrby_condition = IncrbyConditionType.SUCCESS
                            ) as personal_limiter:
        yield personal_limiter
        
        
