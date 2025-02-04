from pydantic import Field, ConfigDict
from core.schemas import BaseModel, UserID, PublicUserInfoOut
from uuid import UUID, uuid4



class VerifyaccessTokenIn(BaseModel):
    
    authorization_header : str | None = Field(default = None)
    

class UserIDIn(BaseModel):
    user_id : UserID
    
    
    
class IssuedJWTTokensDataIn(BaseModel):
    
    user_info : PublicUserInfoOut
    device_id : UUID = Field(default_factory = uuid4)
    jti_acsess_token : UUID = Field(default_factory = uuid4)
    jti_refresh_token : UUID = Field(default_factory = uuid4)
    
    
    
    
    
class RefreshTokenIn(BaseModel):
    
    refresh_token : str = Field(min_length = 1, description = 'refresh_token')
    
    model_config = ConfigDict(title = 'Token Upgrade Form')
    
