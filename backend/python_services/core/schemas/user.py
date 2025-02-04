from pydantic import Field, ConfigDict, EmailStr, AliasChoices
from .BaseModel import BaseModel
from typing import TypeAlias, Annotated
import annotated_types


UserID : TypeAlias = Annotated[int, annotated_types.Ge(1)]




class LoginUserInfo(BaseModel):
    email : EmailStr = Field(min_length = 1, max_length = 255, description = 'User Mail') 


class PublicUserInfo(LoginUserInfo):
    first_name : str = Field(min_length = 1, max_length = 50)
    last_name : str = Field(min_length = 1, max_length = 50)  
    model_config = ConfigDict(title = 'Public User Information')
 

class PublicUserInfoIn(PublicUserInfo):
    pass


class PublicUserInfoOut(PublicUserInfo):
    user_id : UserID = Field(validation_alias = AliasChoices('id', 'user_id'))
    
