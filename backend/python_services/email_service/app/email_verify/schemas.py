from core.schemas import BaseModel
from pydantic import EmailStr, Field, ConfigDict, PositiveInt



class SendEmailIn(BaseModel):
    email : EmailStr = Field(description = 'email for send verify mail')
    model_config     = ConfigDict(title = 'form for send verify mail')
    
    
    
class VerifyCodeIn(BaseModel):
    code : PositiveInt = Field(description = 'mail code')
    email : EmailStr   = Field(description = 'email')
    model_config       = ConfigDict(title = 'code verification form')
    
    
    
class VerifyCodeOut(BaseModel):
    is_correct_code : bool 
    
    
    