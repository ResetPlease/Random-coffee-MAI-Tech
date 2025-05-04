from .errors import (
                        JWTException,
                        TokenRevokedError,
                        IsNotSpecifiedError,
                        ExpiredTokenError,
                        ClientInvalidTokenError,
                        IncorrectTokenTypeError,
                        IncorrectAuthHeaderFromError
                    )
from .schemas import IssuedJWTTokenData, IssuedJWTTokensOut, IssuedJWTTokenPayloadOut, AuthAPIHeaderIn, IssueTokensIn
from .JWTTokenType import JWTTokenType
from .utils import AuthServiceUtils
from .dependences import get_jwttoken_utils
from fastapi import Request, Depends





async def verify_user(
                    request : Request,
                    authorization_header : AuthAPIHeaderIn,
                    jwttoken_utils : AuthServiceUtils = Depends(get_jwttoken_utils)
                ) -> None:
    if request.state._state.get('auth_error') is not None:
        raise request.state.auth_error
    
    if request.state._state.get('user') is not None:
        return
    
    request.state.user = await jwttoken_utils.verify(authorization_header)
    request.state.auth_error = None
    


async def verify_user_if_is_able(
                                request : Request,
                                authorization_header : AuthAPIHeaderIn,
                                jwttoken_utils : AuthServiceUtils = Depends(get_jwttoken_utils)
                            ) -> None:
        request.state.user = None
        request.state.auth_error = None
        
        try:
            request.state.user = await jwttoken_utils.verify(authorization_header)
        except JWTException as error:
            request.state.auth_error = error
            