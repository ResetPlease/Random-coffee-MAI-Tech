from core.schemas import UserID, BaseModel, PublicUserInfoOut, TagID, CorrectDateTimeType, DateTimeIntervalOut, DateTimeIntervalIn
from pydantic import PositiveInt, Field, model_validator, NonNegativeInt, ConfigDict, field_validator
from typing import Self
from app.base import SearchUserIDModel
from datetime import datetime
    
    

class MatchUserOut(SearchUserIDModel, PublicUserInfoOut):
    matched_tags_count : NonNegativeInt
    matched_tag_ids : list[TagID]
    meeting_intervals : list[DateTimeIntervalOut]
    have_planned_meeting : bool
    have_completed_meeting : bool
    
    
    
    
    
class SearchIn(BaseModel):
    min_tags_match : NonNegativeInt = Field(default = 0, le = 100)
    date_start : datetime | None = Field(default = None)
    date_end : datetime | None = Field(default = None)
    time_start : NonNegativeInt | None = Field(default = None, le = 23)
    time_end : NonNegativeInt | None = Field(default = None, le = 23)
    page : PositiveInt = Field(default = 1)
    only_new_users : bool = Field(default = False)
    
    
    @model_validator(mode = 'after')
    def time_validate(self) -> Self:
        
        if self.date_start is not None and self.date_end is not None:
            self.date_start, self.date_end, date_now = map(
                                                lambda date : date.replace(hour = 0, minute = 0, second = 0, microsecond = 0, tzinfo = None), 
                                                (self.date_start, self.date_end, datetime.now())
                                            )
            
            if self.date_start < date_now:
                raise ValueError('Start time passed')
            
            if self.date_start > self.date_end:
                raise ValueError('The end time cannot be more starting')
        else:
            self.date_start, self.date_end = None, None
        
        if self.time_start is None or self.time_end is None:
            self.time_start, self.time_end = None, None
        
        return self
    
    model_config = ConfigDict(frozen = False)
    
   
   

   
   
class UsersMatchingIn(BaseModel):
    meeting_datetime : DateTimeIntervalIn
    searcher_user_id : UserID
    active_user_id : UserID
    
    
    
    
    
                
                
            
    
