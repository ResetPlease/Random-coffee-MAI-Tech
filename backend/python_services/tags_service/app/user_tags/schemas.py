from app.base import TagID, TagModel, TagIDModel
from core.schemas import BaseModel


class UserTagOut(TagIDModel, TagModel):
    pass


class UserTagsListIn(BaseModel):
    tag_ids: list[TagID]


class UserTagsChangeOut(BaseModel):
    changed_tag_ids: list[TagID]
