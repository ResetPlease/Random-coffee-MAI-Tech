from core.schemas import BaseModel, UserID
from enum import StrEnum, auto


class UserBanNotifyType(StrEnum):
    BAN = auto()
    UNBAN = auto()




class UserBanNotify(BaseModel):
    status : UserBanNotifyType
    blocked_user_id : UserID
    blocker_user_id : UserID