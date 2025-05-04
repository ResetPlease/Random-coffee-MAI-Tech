from .dao import MeetingDAO, MeetingMembersDAO, MeetingConcatinateDAO
from functools import lru_cache
from fastapi import Depends
from .utils import MeetingUtils
from core.dao.http import HTTPRequest



@lru_cache
def get_meeting_dao() -> MeetingDAO:
    return MeetingDAO()


@lru_cache
def get_meeting_members_dao() -> MeetingMembersDAO:
    return MeetingMembersDAO()


@lru_cache
def get_meeting_concatinate_dao(
                                meeting_dao : MeetingDAO = Depends(get_meeting_dao),
                                meeting_members_dao : MeetingMembersDAO = Depends(get_meeting_members_dao)
                                ) -> MeetingConcatinateDAO:
    return MeetingConcatinateDAO(meeting_dao, meeting_members_dao)


@lru_cache
def get_meeting_utils() -> MeetingUtils:
    from core.services.search import search_service_settings
    
    return MeetingUtils(
                                HTTPRequest(), 
                                search_service_settings.NAME, 
                                search_service_settings.PORT,
                                search_service_settings.MATCH_ENDPOINT,
                                search_service_settings.MATCH_ENDPOINT_METHOD
                            )