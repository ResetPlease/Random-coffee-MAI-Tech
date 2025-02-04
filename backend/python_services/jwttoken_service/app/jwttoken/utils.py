import jwt
from datetime import datetime, timedelta
from .JWTTokenType import JWTTokenType
from .config import jwtsettings
from core.dependencies.JWTToken import (
                                        IssuedJWTTokenData,
                                        IssuedJWTTokensOut,
                                        IssuedJWTTokenPayloadOut,
                                        IsNotSpecifiedError,
                                        IncorrectAuthHeaderFromError,
                                        ExpiredTokenError,
                                        ClientInvalidTokenError,
                                        IncorrectTokenTypeError
                                    )
from jwt import ExpiredSignatureError, InvalidTokenError
from core.schemas import PublicUserInfoOut
from .schemas import IssuedJWTTokensDataIn
from datetime import datetime
import logging




class JWTToken:
    
    
    @classmethod
    def generate_access_token(cls, token_data : IssuedJWTTokenData, user_info : PublicUserInfoOut) -> str:
        return cls.__sign_token(
            type = JWTTokenType.ACCESS,
            token_data = token_data,
            user_info = user_info,
            ttl = jwtsettings.ACCESS_TOKEN_TTL
        )
        
        
    
    @classmethod
    def generate_refresh_token(cls, token_data : IssuedJWTTokenData, user_info : PublicUserInfoOut) -> str:
        return cls.__sign_token(
            type = JWTTokenType.REFRESH,
            token_data = token_data,
            user_info = user_info,
            ttl = jwtsettings.REFRESH_TOKEN_TTL
        )
      
        
    
    @staticmethod
    def verify_token(token : str) -> dict[str, str | int]:
        return jwt.decode(jwt = token, key = jwtsettings.SECRET, algorithms = [jwtsettings.ALGORITHM])



    @classmethod
    def get_jti(cls, token : str) -> str:
        return cls.verify_token(token)['jti']



    @classmethod
    def get_sub(cls, token : str) -> str:
        return cls.verify_token(token)['sub']



    @classmethod
    def get_exp(cls, token : str) -> int:
        return cls.verify_token(token)['exp']
    
    
    
    @classmethod
    def is_active_token(cls, token : str) -> bool:
        return (cls.get_exp(token) - cls.get_numeric_date_time_now()) > 0
    
    
    
    @staticmethod
    def get_numeric_date_time_now() -> int:
        return int(datetime.now().timestamp())
    
    
    
    @classmethod
    def __sign_token(
                    cls,
                    type: JWTTokenType,
                    token_data : IssuedJWTTokenData,
                    user_info : PublicUserInfoOut,
                    ttl : timedelta
                ) -> str:
        numeric_date_time_now = cls.get_numeric_date_time_now()
        
        default_payload = {
            'type' : type,
            'iat' : numeric_date_time_now,
            'exp' : numeric_date_time_now  + int(ttl.total_seconds())
        }
        full_payload = default_payload | user_info.model_dump() | token_data.model_dump(mode = 'json')

        logging.info(full_payload)
        
        return jwt.encode(payload = full_payload, key = jwtsettings.SECRET, algorithm = jwtsettings.ALGORITHM)
    
    
    
    
    @classmethod
    def generate_tokens(
                        cls,
                        tokens_data : IssuedJWTTokensDataIn
                    ) -> IssuedJWTTokensOut:
        
        access_token_data = IssuedJWTTokenData(device_id = tokens_data.device_id, jti = tokens_data.jti_acsess_token)
        refresh_token_data = IssuedJWTTokenData(device_id = tokens_data.device_id, jti = tokens_data.jti_refresh_token)

        return IssuedJWTTokensOut(
                            access_token = JWTToken.generate_access_token(access_token_data, tokens_data.user_info),
                            refresh_token = JWTToken.generate_refresh_token(refresh_token_data, tokens_data.user_info),
                            exp = cls.get_numeric_date_time_now() + jwtsettings.ACCESS_TOKEN_TTL.total_seconds()
                        )
        
    
    
    
    

class TokenValidation:



    @staticmethod
    def __try_to_get_clear_token(authorization_header: str) -> str:
        if authorization_header is None:
            raise IsNotSpecifiedError

        if 'Bearer ' not in authorization_header:
            raise IncorrectAuthHeaderFromError

        return authorization_header.removeprefix('Bearer ')



    @classmethod
    def get_token_payload(cls, authorization_header : str, type_ : JWTTokenType) -> IssuedJWTTokenPayloadOut:
        token = cls.__try_to_get_clear_token(authorization_header)
        
        try:
            payload = JWTToken.verify_token(token)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        
        except InvalidTokenError:
            raise ClientInvalidTokenError
        
        if payload['type'] != type_:
            raise IncorrectTokenTypeError

        return IssuedJWTTokenPayloadOut.model_validate(payload)
    
    
    
