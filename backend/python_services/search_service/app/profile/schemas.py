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
        sorted_meeting_intervals = sorted(meeting_intervals, key = lambda interval : interval.start)
        for index in range(len(meeting_intervals) - 1):
            meeting_interval_now = sorted_meeting_intervals[index]
            meeting_interval_next = sorted_meeting_intervals[index + 1]
            
            if meeting_interval_now.end > meeting_interval_next.start:
                raise ValueError('Intersecting intervals')
            
        for meeting_interval in sorted_meeting_intervals:
            if (meeting_interval.end - meeting_interval.start).days > 0:
                raise ValueError('Too large time interval')
        
        return meeting_intervals
                
            