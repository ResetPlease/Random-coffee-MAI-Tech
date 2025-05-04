from core.schemas import BaseModel, DateTimeIntervalIn
from app.base import SearchUserProfileInfo
from pydantic import computed_field, NonNegativeInt, field_validator




class SearchUserProfileOut(BaseModel):
    information : SearchUserProfileInfo | None

    
    
class SearchUserProfileIn(SearchUserProfileInfo):
    meeting_intervals : list[DateTimeIntervalIn]
    min_tags_match : NonNegativeInt
    
    
    @field_validator('meeting_intervals', mode = 'after')
    @classmethod
    def check_valid_meeting_intervals(cls, meeting_intervals : list[DateTimeIntervalIn]) -> None:
        for meeting_interval_now in meeting_intervals:
            if (meeting_interval_now.end - meeting_interval_now.start).days > 0:
                raise ValueError('Too large time interval')
        
        return meeting_intervals
                
            