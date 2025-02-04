from fastapi import APIRouter, Request, Depends
from core.dependencies.JWTToken import IssuedJWTTokensOut, JWTException, IssuedJWTTokenPayloadOut
from .dao import JWTTokenDAO
from .dependencies import check_secret_key
from .schemas import VerifyaccessTokenIn, UserIDIn, RefreshTokenIn
from .errors import IssueException


router = APIRouter(
                    tags = ['Work with tokens']
                )



@router.post(
            path = '/issue',
            summary = 'Issue tokens',
            dependencies = [Depends(check_secret_key)],
            responses = IssueException.get_responses_schemas()
        )
async def issue_tokens(body : UserIDIn) -> IssuedJWTTokensOut:
    return await JWTTokenDAO.issue_tokens(user_id = body.user_id)



@router.post(path = '/verify', summary = 'Verify token', responses = JWTException.get_responses_schemas())
async def verify_access_token(request : Request, body : VerifyaccessTokenIn) -> IssuedJWTTokenPayloadOut:
    return await JWTTokenDAO.verify_access_token(authorization_header = body.authorization_header)



@router.post(path = '/update', summary = 'Tokens update', responses = JWTException.get_responses_schemas())
async def update_tokens(token : RefreshTokenIn) -> IssuedJWTTokensOut:
    return await JWTTokenDAO.update_tokens(refresh_token = token.refresh_token)






