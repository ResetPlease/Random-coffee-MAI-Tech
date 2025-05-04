from pydantic import Field, ConfigDict
from uuid import UUID
from core.schemas import BaseModel, PublicUserInfoOut
from typing import Annotated, TypeAlias
from fastapi import Security
from fastapi.security import APIKeyHeader



class IssuedJWTTokenData(BaseModel):
    
    jti : UUID = Field(description = 'Token UUID')
    device_id : UUID = Field(description = 'Device Identifier')
    version : UUID = Field(description = 'Token version')
    
    model_config = ConfigDict(title = 'Token Information')
    
    
class IssuedJWTTokenPayloadOut(IssuedJWTTokenData, PublicUserInfoOut):
    pass
    
    
    
class IssuedJWTTokensOut(BaseModel):
    
    access_token : str = Field(description = 'access_token')
    refresh_token : str = Field(description = 'refresh_token')
    exp : float = Field(description = 'Lifetime access_token')
    
    model_config = ConfigDict(title = 'Generated access_token and refresh_token')
    
    
    
class IssueTokensIn(PublicUserInfoOut):
    pass
    
    
    
AuthAPIHeaderIn : TypeAlias = Annotated[str | None, Security(APIKeyHeader(name = 'Authorization', auto_error = False, scheme_name = 'User Authorization'))]
    
    