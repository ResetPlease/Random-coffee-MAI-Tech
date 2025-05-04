from core.schemas import UserID, BaseModel, PublicUserInfoOut
from pydantic import Field



class UserBlockingIn(BaseModel):
    blocked_id : UserID = Field(description = 'The user ID must be blocked')
    
    