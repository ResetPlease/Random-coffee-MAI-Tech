from fastapi import APIRouter
from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, UserChangePasswordIn, UserVerifyPasswordIn
from .dao import AuthDAO
from .errors import AuthException
from core.dependencies.JWTToken import IssuedJWTTokensOut
from .dependencies import verify_code


router = APIRouter(
                    tags = ['Authentication'],
                    responses = AuthException.get_responses_schemas()
                )






@router.post(path = '/registration', summary = 'User registration')
async def registrate(user_credentials : UserRegistrationCredentialsIn) -> IssuedJWTTokensOut:
    await verify_code(UserVerifyPasswordIn.model_validate(user_credentials))
    user_id = await AuthDAO.registrate(user_credentials = user_credentials)
    return await AuthDAO.get_tokens(user_id)





@router.post(path = '/login', summary = 'Sign in to your account')
async def login(user_credentials : UserLoginCredentialsIn) -> IssuedJWTTokensOut:
    await verify_code(UserVerifyPasswordIn.model_validate(user_credentials))
    user_id = await AuthDAO.login(user_credentials = user_credentials)
    return await AuthDAO.get_tokens(user_id)



@router.post(path = '/change-password', summary = 'Change password')
async def change_password(user_credentials : UserChangePasswordIn) -> IssuedJWTTokensOut:
    await verify_code(UserVerifyPasswordIn.model_validate(user_credentials))
    user_id = await AuthDAO.change_password(user_credentials = user_credentials)
    return await AuthDAO.get_tokens(user_id)





