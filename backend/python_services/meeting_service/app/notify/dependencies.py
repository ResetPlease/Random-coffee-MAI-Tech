from .utils import UserBanNotifyUtils, MeetingNotifyUtils
from functools import lru_cache




@lru_cache
def get_user_ban_notify_utils() -> UserBanNotifyUtils:
    from core.models.rabbitmq.ban import ban_publisher
    
    return UserBanNotifyUtils(ban_publisher)


@lru_cache
def get_meeting_notify_utils() -> MeetingNotifyUtils:
    from core.models.rabbitmq.meeting import meeting_publisher
    
    return MeetingNotifyUtils(meeting_publisher)

