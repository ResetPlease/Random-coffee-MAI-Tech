
from fastapi import Request, Depends, Body
from core.schemas import LoginUserInfo
from core.dependencies.limiter import RequestLimiter, PersonalLimiter, IncrbyConditionType, UnblockConditionType
from .errors import MaxAttemptsEnterPasswordError, InvalidPasswordError, AccessBlockedError  
from .dao import AuthenticationDAO
from .utils import AuthenticationUtils, NewUserNotifyUtils
from functools import lru_cache
from typing import AsyncGenerator
from app.jwttoken.dependencies import get_jwttoken_action_utils, JWTTokenActionsUtils, get_jwttoken_dao, JWTTokenDAO
from .schemas import UserVerifyAccessIn
from app.user_verify.dependencies import get_user_verifying_dao, UserVerifyingDAO
from core.dependencies.JWTToken import AuthAPIHeaderIn, JWTException
from core.exception import BaseHTTPException
import logging



@lru_cache
def get_auth_dao() -> AuthenticationDAO:
    auth_utils = AuthenticationUtils()
    return AuthenticationDAO(auth_utils)



@lru_cache
def get_new_user_notify_utils() -> NewUserNotifyUtils:
    from core.models.rabbitmq.user import create_user_publisher
    
    return NewUserNotifyUtils(create_user_publisher)
            
                               



@lru_cache
def get_auth_request_limiter() -> RequestLimiter:
    from .config import auth_settings
    
    return RequestLimiter(
                        (auth_settings.FIRST_BLOCK_TIME, auth_settings.MAX_PASSWORD_FAIL_ATTEMPT_BEFORE_FIRST_BLOCK),
                        (auth_settings.SECOND_BLOCK_TIME, auth_settings.MAX_PASSWORD_FAIL_ATTEMPT_BEFORE_SECOND_BLOCK),
                        block_lifetime = auth_settings.BLOCK_LIFETIME
                    )




async def get_login_limit(
                            user_credentials : LoginUserInfo,
                            auth_request_limiter : RequestLimiter = Depends(get_auth_request_limiter)
                        ) -> AsyncGenerator[PersonalLimiter, None]:
    async with auth_request_limiter(
                                    '/api/auth/login', 
                                    user_credentials.email, 
                                    block_error = MaxAttemptsEnterPasswordError,
                                    incrby_condition = IncrbyConditionType.ERROR,
                                    unblock_condition = UnblockConditionType.SUCCESS,
                                    incrby_trigger_errors = [InvalidPasswordError]
                                ) as login_limiter:
        yield login_limiter
        
        


async def get_unclock_login_limit(
                            user_credentials : LoginUserInfo,
                            auth_request_limiter : RequestLimiter = Depends(get_auth_request_limiter)
                        ) -> AsyncGenerator[PersonalLimiter, None]:
    async with auth_request_limiter(
                                    '/api/auth/login', 
                                    user_credentials.email,
                                    incrby_condition = IncrbyConditionType.NEVER,
                                    unblock_condition = UnblockConditionType.SUCCESS
                                ) as unblock_limiter:
        yield unblock_limiter
        
        

async def check_user_access(
                            user_credentials : UserVerifyAccessIn,
                            verify_dao : UserVerifyingDAO = Depends(get_user_verifying_dao)
                        ) -> AsyncGenerator[None, None]:
    email, operation_id = user_credentials.email, user_credentials.operation_id
    is_access = operation_id is not None and await verify_dao.delete_user_verification(email, operation_id)
    
    if not is_access:
        raise AccessBlockedError
    try:
        yield 
    except BaseHTTPException as error:
        await verify_dao.save_user_verification(email, operation_id)
        raise error from None
    
    
        
        

async def check_user_change_password_access(
                                            auth_header : AuthAPIHeaderIn,
                                            user_credentials : UserVerifyAccessIn,
                                            verify_dao : UserVerifyingDAO = Depends(get_user_verifying_dao),
                                            jwttoken_dao : JWTTokenDAO = Depends(get_jwttoken_dao),
                                            jwttoken_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
                                        ) -> AsyncGenerator[None, None]:
    try:
        payload = await jwttoken_utils.verify_access_token(auth_header)
    except JWTException:
        payload = None
        
    if payload is None or payload.email != user_credentials.email:
        check_user_access_generator = check_user_access(user_credentials, verify_dao)
        await anext(check_user_access_generator)
        
        try:
            yield 
        except BaseHTTPException as error:
            await check_user_access_generator.athrow(error)
        
    else:
        yield 
        await jwttoken_dao.delete_token(payload.user_id, payload.device_id)
    


        
        



        
        