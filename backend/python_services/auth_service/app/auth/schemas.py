from pydantic import Field, ConfigDict, field_serializer, field_validator, PositiveInt
from core.schemas import BaseModel, LoginUserInfo, PublicUserInfoIn
from hashlib import sha256


class UserCredentialsIn(BaseModel):
    password : str = Field(serialization_alias = 'hash_password', min_length = 5, max_length = 50, description = 'Password')
    
    @field_serializer('password')
    @classmethod
    def password_serialize(cls, password : str) -> str:
        return sha256(str.encode(password)).hexdigest()
    

class UserVerifyPasswordIn(LoginUserInfo):
    code : PositiveInt = Field(exclude = True, description = 'email verify code')
    



class UserLoginCredentialsIn(UserCredentialsIn, UserVerifyPasswordIn):
    model_config = ConfigDict(title = 'Login to the account')
    



class UserRegistrationCredentialsIn(PublicUserInfoIn, UserCredentialsIn, UserVerifyPasswordIn):
    model_config = ConfigDict(title = 'Creating an account')
        
        
        
class UserChangePasswordIn(UserCredentialsIn, UserVerifyPasswordIn):
    model_config = ConfigDict(title = 'Change password')
    
    

    

   
    

    

