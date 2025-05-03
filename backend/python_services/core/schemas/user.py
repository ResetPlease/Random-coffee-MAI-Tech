from pydantic import Field, ConfigDict, EmailStr, AliasChoices, field_validator
from .BaseModel import BaseModel
from .model_types import UserID, StrXSS



class LoginUserInfo(BaseModel):
    email : EmailStr = Field(min_length = 1, max_length = 255, description = 'User Mail') 


class PublicUserInfo(LoginUserInfo):
    model_config = ConfigDict(title = 'Public User Information')
 

class PublicUserInfoIn(PublicUserInfo):
    first_name : StrXSS = Field(min_length = 1, max_length = 50)
    last_name  : StrXSS = Field(min_length = 1, max_length = 50)
    

class PublicUserInfoOut(PublicUserInfo):
    first_name : str
    last_name  : str  
    user_id : UserID = Field(validation_alias = AliasChoices('id', 'user_id'))
    
