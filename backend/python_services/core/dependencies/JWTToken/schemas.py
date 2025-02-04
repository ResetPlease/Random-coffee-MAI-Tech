from pydantic import Field, ConfigDict
from uuid import UUID
from core.schemas import BaseModel, PublicUserInfoOut



class IssuedJWTTokenData(BaseModel):
    
    jti : UUID = Field(description = 'Token UUID')
    device_id : UUID = Field(description = 'Device Identifier')
    
    model_config = ConfigDict(title = 'Token Information')
    
    
class IssuedJWTTokenPayloadOut(IssuedJWTTokenData, PublicUserInfoOut):
    pass
    
    
    
class IssuedJWTTokensOut(BaseModel):
    
    access_token : str = Field(description = 'access_token')
    refresh_token : str = Field(description = 'refresh_token')
    exp : float = Field(description = 'Lifetime access_token')
    
    model_config = ConfigDict(title = 'Generated access_token and refresh_token')
    
    
    
    
