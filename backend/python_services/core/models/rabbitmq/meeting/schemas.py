from core.schemas import MeetingID, UserID, BaseModel
from enum import StrEnum, auto


class MeetingStatusType(StrEnum):
    CANCEL = auto()
    COMPLETE = auto()



class NewMeetingNotify(BaseModel):
    meeting_id : MeetingID
    members : list[UserID]
    
    
class MeetingNotify(BaseModel):
    meeting_id : MeetingID
    status : MeetingStatusType
    
    