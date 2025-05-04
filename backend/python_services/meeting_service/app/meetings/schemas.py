from core.schemas import BaseModel, PublicUserInfoOut, MeetingID, UserID, DateTimeIntervalIn, DateTimeIntervalOut
from pydantic import Field, AliasChoices
from datetime import datetime 
from core.models.postgres import MeetingStatusType


class MeetingIn(BaseModel):
    meeting_datetime : DateTimeIntervalIn
    meeting_user_id : UserID
    

class ChangeMeetingStatusIn(BaseModel):
    meeting_id : MeetingID
    

class SuccessMeetingCreateOut(BaseModel):
    meeting_id : MeetingID


class MeetingOut(BaseModel):
    meeting_id : int = Field(alias = AliasChoices('id', 'meeting_id'))
    meeting_datetime : DateTimeIntervalOut
    status : MeetingStatusType
    created_at : datetime
    
    users : list[PublicUserInfoOut]

