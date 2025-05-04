from .dao import UpdateUsersDAO, MeetingsDAO, UsersMeetingConcatinateDAO
from .utils import UpdateUsersUtils
from app.profile.dao import SearchProfileDAO
from app.profile.dependencies import get_search_profile_dao
from functools import lru_cache
from fastapi import Depends



@lru_cache
def get_change_users_dao() -> UpdateUsersDAO:
    return UpdateUsersDAO()


@lru_cache
def get_meeting_dao() -> MeetingsDAO:
    return MeetingsDAO()


@lru_cache
def get_user_meeting_concatinate_dao(
                                    user_dao : UpdateUsersDAO = Depends(get_change_users_dao),
                                    meeting_dao : MeetingsDAO = Depends(get_meeting_dao),
                                    search_profile_dao : SearchProfileDAO = Depends(get_search_profile_dao)
                                ) -> UsersMeetingConcatinateDAO:
    return UsersMeetingConcatinateDAO(user_dao, meeting_dao, search_profile_dao)


@lru_cache
def get_update_users_utils() -> UpdateUsersUtils:
    from app.base.config import search_service_settings
    
    return UpdateUsersUtils(search_service_settings.NACK_MESSAGE_BLOCK_SECONDS)