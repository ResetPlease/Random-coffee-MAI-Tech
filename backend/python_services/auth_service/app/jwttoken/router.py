from fastapi import APIRouter, Depends
from core.dependencies.JWTToken import (
                                        IssuedJWTTokensOut, 
                                        JWTException, 
                                        IssuedJWTTokenPayloadOut, 
                                        AuthAPIHeaderIn, 
                                        IssueTokensIn
                                    )
from .schemas import UpdateTokensIn
from core.schemas import UserActionOut
from .dependencies import get_jwttoken_action_utils
from .utils import JWTTokenActionsUtils



router = APIRouter(
                    prefix = '/token',
                    tags = ['Work with tokens']
                )





@router.get(
            path = '',
            summary = 'Verify token',
            responses = JWTException.get_responses_schemas()
        )
async def verify_access_token(
                                authorization_header : AuthAPIHeaderIn, 
                                jwttoken_action_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
                            ) -> IssuedJWTTokenPayloadOut:
    return await jwttoken_action_utils.verify_access_token(authorization_header)




@router.post(
            path = '/update',
            summary = 'Token update',
            responses = JWTException.get_responses_schemas()
        )
async def update_tokens(
                        form : UpdateTokensIn, 
                        jwttoken_action_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
                    ) -> IssuedJWTTokensOut:
    return await jwttoken_action_utils.update_tokens(refresh_token = form.refresh_token)




@router.post(
            path = '/revoke',
            summary = 'Revoke token',
            responses = JWTException.get_responses_schemas()
        )
async def revorke_token(
                    authorization_header : AuthAPIHeaderIn, 
                    jwttoken_action_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
                ) -> UserActionOut:
    await jwttoken_action_utils.delete_token(authorization_header)
    return UserActionOut()



@router.post(
            path = '/revoke/all',
            summary = 'Revoke all user tokens',
            responses = JWTException.get_responses_schemas()
        )
async def delete_all_user_tokens(
                            authorization_header : AuthAPIHeaderIn, 
                            jwttoken_action_utils : JWTTokenActionsUtils = Depends(get_jwttoken_action_utils)
                        ) -> UserActionOut:
    await jwttoken_action_utils.delete_all_user_tokens(authorization_header)
    return UserActionOut()






