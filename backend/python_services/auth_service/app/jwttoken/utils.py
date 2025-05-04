from datetime import datetime, timedelta
from core.dependencies.JWTToken import (
                                        IssuedJWTTokenData,
                                        IssuedJWTTokensOut,
                                        IssuedJWTTokenPayloadOut,
                                        JWTTokenType,
                                        IssueTokensIn,
                                        IsNotSpecifiedError,
                                        IncorrectAuthHeaderFromError,
                                        ExpiredTokenError,
                                        ClientInvalidTokenError,
                                        IncorrectTokenTypeError,
                                        AuthAPIHeaderIn
                                    )
from jwt import ExpiredSignatureError, InvalidTokenError, decode, encode
from core.schemas import PublicUserInfoOut
from datetime import datetime
from uuid import UUID, uuid4
from .dao import JWTTokenDAO





class JWTTokenRandomFields:
    
    
    @staticmethod
    def get_jti() -> UUID:
        return uuid4()
    
    
    @staticmethod
    def get_device_id() -> UUID:
        return uuid4()
        
    
    @staticmethod
    def get_version() -> UUID:
        return uuid4()
    
    
    



class JWTTokenUtils:
    
    __slots__ = ('type_', 'ttl', 'secret', 'algorithm')
    
    def __init__(
                    self, 
                    type_ : JWTTokenType,
                    ttl : timedelta,
                    secret : str,
                    algorithm : str
                ) -> None:
        self.type_ = type_
        self.ttl = ttl
        self.secret = secret
        self.algorithm = algorithm
        
        
    
    def get_time_now(self) -> int:
        return int(datetime.now().timestamp())
    
    
    def get_lifetime(self) -> int:
        return int(self.ttl.total_seconds())
    
    
    def get_expired_time(self) -> int:
        return self.get_time_now() + self.get_lifetime()
    
    
    
    def _verify_token(self, token : str) -> dict[str, str | int]:
        return decode(jwt = token, key = self.secret, algorithms = self.algorithm)
        
    
    
    def generate(
                self,
                token_data : IssuedJWTTokenData,
                user_info : PublicUserInfoOut
            ) -> str:
        
        default_payload = {
                        'type' : self.type_,
                        'iat' : self.get_time_now(),
                        'exp' : self.get_expired_time()
                    }
        full_payload = default_payload | user_info.model_dump() | token_data.model_dump(mode = 'json')
        
        return encode(payload = full_payload, key = self.secret, algorithm = self.algorithm)
    
    
    
    def validate(self, token : str) -> IssuedJWTTokenPayloadOut:
        try:
            payload = self._verify_token(token)
        except ExpiredSignatureError:
            raise ExpiredTokenError
        
        except InvalidTokenError:
            raise ClientInvalidTokenError
        
        if payload['type'] != self.type_:
            raise IncorrectTokenTypeError

        return IssuedJWTTokenPayloadOut.model_validate(payload)
        




class AccessTokenUtils(JWTTokenUtils):
    
    __slots__ = ()
    
    def __init__(
                    self, 
                    ttl : timedelta,
                    secret : str,
                    algorithm : str
                ) -> None:
        super().__init__(JWTTokenType.ACCESS, ttl, secret, algorithm)
    
    
    def validate(self, token : str | None) -> IssuedJWTTokenPayloadOut:
        if token is None:
            raise IsNotSpecifiedError

        if 'Bearer ' not in token:
            raise IncorrectAuthHeaderFromError

        return super().validate(token.removeprefix('Bearer '))





class RefreshTokenUtils(JWTTokenUtils):
    
    __slots__ = ()
    
    def __init__(
                    self, 
                    ttl : timedelta,
                    secret : str,
                    algorithm : str
                ) -> None:
        super().__init__(JWTTokenType.REFRESH, ttl, secret, algorithm)
        
        


        
class JWTTokensConcatenateUtils:
    
    __slots__ = ('access', 'refresh', 'random_generator')
    
    def __init__(
                    self, 
                    access : JWTTokenUtils, 
                    refresh : JWTTokenUtils, 
                    random_generator : JWTTokenRandomFields
                ) -> None:
        self.access = access
        self.refresh = refresh
        self.random_generator = random_generator
        
    
    def generate(
                    self,
                    user_info : PublicUserInfoOut, 
                    device_id : UUID | None = None, 
                    version : UUID | None = None, 
                    access_token_jti : UUID | None = None, 
                    refresh_token_jti : UUID | None = None
                ) -> IssuedJWTTokensOut: 
        device_id = device_id or self.random_generator.get_device_id()
        version = version or self.random_generator.get_version()
        
        access_token_data = IssuedJWTTokenData(device_id = device_id, version = version, jti = access_token_jti or self.random_generator.get_jti())
        refresh_token_data = IssuedJWTTokenData(device_id = device_id, version = version, jti = refresh_token_jti or self.random_generator.get_jti())
        
        return IssuedJWTTokensOut(
                            access_token = self.access.generate(access_token_data, user_info),
                            refresh_token = self.refresh.generate(refresh_token_data, user_info),
                            exp = self.access.get_expired_time()
                        )
        
        


class JWTTokenActionsUtils:
    
    __slots__ = ('jwttoken_utils', 'jwttoken_dao')
    

    def __init__(
                self, 
                jwttoken_utils : JWTTokensConcatenateUtils,
                jwttoken_dao : JWTTokenDAO
            ) -> None:
        self.jwttoken_dao = jwttoken_dao
        self.jwttoken_utils = jwttoken_utils
        
    
    async def issue_tokens(self, user_info : IssueTokensIn) -> IssuedJWTTokenPayloadOut:
        device_id, version = self.jwttoken_utils.random_generator.get_device_id(), self.jwttoken_utils.random_generator.get_version()
        await self.jwttoken_dao.save_token(user_info.user_id, device_id, version)
        return self.jwttoken_utils.generate(user_info, device_id, version)
    
    
    async def verify_access_token(self, authorization_header : AuthAPIHeaderIn) -> IssuedJWTTokenPayloadOut:
        
        payload = self.jwttoken_utils.access.validate(authorization_header)
        await self.jwttoken_dao.verify_token(payload.user_id, payload.device_id, payload.version)
        return payload
    
    
    async def update_tokens( 
                            self,
                            refresh_token : str
                        ) -> IssuedJWTTokensOut:
        payload = self.jwttoken_utils.refresh.validate(refresh_token)
        new_token_version = self.jwttoken_utils.random_generator.get_version()
        await self.jwttoken_dao.update_token(payload.user_id, payload.device_id, payload.version, new_token_version)
        return self.jwttoken_utils.generate(PublicUserInfoOut.model_validate(payload), payload.device_id, new_token_version)



    async def delete_token(self, authorization_header : AuthAPIHeaderIn) -> None:
        payload = await self.verify_access_token(authorization_header)
        await self.jwttoken_dao.delete_token(payload.user_id, payload.device_id)
        
    
    async def delete_all_user_tokens(self, authorization_header : AuthAPIHeaderIn) -> None:
        payload = await self.verify_access_token(authorization_header)
        await self.jwttoken_dao.delete_all_user_tokens(payload.user_id)