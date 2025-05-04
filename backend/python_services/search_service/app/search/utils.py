from pydantic import PositiveInt
from app.base.schemas import ActiveSearchUserOut, SearchUserOut
from .errors import ( 
                    SameUserIDError,
                    NotActiveUserError,
                    MatchException,
                    IncorrectDatetimeError,
                    UserBannedError,
                    MatchTagsError
                )
from app.base import IncorrectUserIDError
from datetime import datetime




class SearchUtils:
    
    __slots__ = ('page_size', )
    
    def __init__(self, page_size : PositiveInt) -> None:
        self.page_size = page_size
        
        
    def convert_page_to_skip_and_limit(self, page : PositiveInt) -> tuple[PositiveInt, PositiveInt]:
        
        return (page - 1) * self.page_size, self.page_size
        
    
    
    def is_two_users_can_start_meeting(
                                    self, 
                                    searcher_user : SearchUserOut | None, 
                                    active_user : ActiveSearchUserOut | None,
                                    start_meeting_datetime : datetime,
                                    end_meeting_datetime : datetime
                                ) -> MatchException | None:
        if searcher_user is None:
            return IncorrectUserIDError
        
        if active_user is None:
            return NotActiveUserError
        
        if searcher_user.user_id == active_user.user_id:
            return SameUserIDError

        if active_user.user_id in searcher_user.banned_user_ids or searcher_user.user_id in active_user.banned_user_ids:
            return UserBannedError
        
        users_tags_intersection = set(active_user.tag_ids) & set(searcher_user.tag_ids)
        
        if len(users_tags_intersection) < active_user.min_tags_match:
            return MatchTagsError
        
        for meeting_interval in active_user.meeting_intervals:
            if meeting_interval.start <= start_meeting_datetime and end_meeting_datetime <= meeting_interval.end:
                return
        
        return IncorrectDatetimeError
