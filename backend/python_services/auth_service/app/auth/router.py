from fastapi import APIRouter, Depends
from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, UserChangePasswordIn
from .dao import AuthenticationDAO
from .errors import AuthException
from core.dependencies.JWTToken import IssueTokensIn, IssuedJWTTokensOut
from app.jwttoken.dependencies import get_jwttoken_action_utils, JWTTokenActionsUtils
from .dependencies import (
                            get_auth_dao, 
                            get_login_limit,
                            get_unclock_login_limit,
                            check_user_access,
                            check_user_change_password_access,
                            get_new_user_notify_utils
                        )
from core.schemas import UpdateUserActionOut
from .utils import NewUserNotifyUtils
import asyncio




router = APIRouter(
                    tags = ['Authentication'],
                    responses = AuthException.get_responses_schemas()
                )






@router.post(
                path = '/registration',
                summary = 'User registration',
                dependencies = [Depends(check_user_access)]
            )
async def registrate(
                    user_credentials : UserRegistrationCredentialsIn,
                    auth_dao : AuthenticationDAO = Depends(get_auth_dao),
                    tokens_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils),
                    notify_utils : NewUserNotifyUtils = Depends(get_new_user_notify_utils)
                ) -> IssuedJWTTokensOut:
    user_id = await auth_dao.create_new_user(user_credentials = user_credentials)
    issue_tokens_form = IssueTokensIn.model_validate(user_credentials.model_dump() | {'user_id' : user_id})
    
    tokens, _  = await asyncio.gather(
                                tokens_utils.issue_tokens(issue_tokens_form),
                                notify_utils.notify(issue_tokens_form)
                            )
    return tokens





@router.post(
                path = '/login', 
                summary = 'Sign in to account',
                dependencies = [Depends(get_login_limit)]
            )
async def login(
                user_credentials : UserLoginCredentialsIn, 
                auth_dao : AuthenticationDAO = Depends(get_auth_dao),
                tokens_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
            ) -> IssuedJWTTokensOut:
    user_db = await auth_dao.get_user_by_email(user_credentials.email, user_credentials.password)
    return await tokens_utils.issue_tokens(IssueTokensIn.model_validate(user_db))





@router.post(
                path = '/change-password', 
                summary = 'Change password',
                dependencies = [Depends(get_unclock_login_limit), Depends(check_user_change_password_access)]
            )
async def change_password(
                            user_credentials : UserChangePasswordIn,
                            auth_dao : AuthenticationDAO = Depends(get_auth_dao)
                        ) -> UpdateUserActionOut:
    await auth_dao.change_user_password(user_credentials.email, user_credentials.password)
    return UpdateUserActionOut()





