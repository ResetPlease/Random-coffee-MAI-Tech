from core.schemas import UserID, BaseModel, PublicUserInfoOut, TagID, CorrectDateTimeType, DateTimeIntervalOut, DateTimeIntervalIn
from datetime import datetime
from pydantic import Field, NonNegativeInt





class SearchUserIDModel(BaseModel):
    user_id : UserID = Field(validation_alias = '_id')



class SearchUserOut(SearchUserIDModel, PublicUserInfoOut):
    tag_ids : list[TagID] 
    banned_user_ids : list[UserID]



class SearchUserProfileInfo(BaseModel):
    meeting_intervals : list[DateTimeIntervalOut]
    min_tags_match : NonNegativeInt


class ActiveSearchUserOut(SearchUserProfileInfo, SearchUserOut):
    pass