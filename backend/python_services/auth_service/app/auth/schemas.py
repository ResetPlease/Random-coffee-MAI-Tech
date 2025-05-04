from pydantic import Field, ConfigDict, field_validator
from core.schemas import BaseModel, LoginUserInfo, PublicUserInfoIn, Str
from uuid import UUID



class UserCredentialsIn(BaseModel):
    password : Str = Field(exclude = True, min_length = 5, max_length = 50, description = 'Password')
    
    

class UserVerifyAccessIn(LoginUserInfo):
    operation_id : UUID | None = Field(exclude = True, default = None)
    

class UserLoginCredentialsIn(UserCredentialsIn, LoginUserInfo):
    model_config = ConfigDict(title = 'Logining to the account')
    


class UserRegistrationCredentialsIn(UserCredentialsIn, UserVerifyAccessIn, PublicUserInfoIn):
    model_config = ConfigDict(title = 'Creating an account')
        
        
        
class UserChangePasswordIn(UserCredentialsIn, UserVerifyAccessIn, LoginUserInfo):
    model_config = ConfigDict(title = 'Change password')
    


    

