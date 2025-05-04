from core.schemas import TagID, BaseModel, UserID
from enum import StrEnum, auto



class TagsChangeNotifyType(StrEnum):
    ADD = auto()
    DELETE = auto()




class ChangeUserTagsNotify(BaseModel):
    status : TagsChangeNotifyType
    user_id : UserID
    tag_ids : list[TagID]
    