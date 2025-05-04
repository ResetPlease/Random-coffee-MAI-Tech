from app.base import TagModel, TagIDModel
from core.schemas import BaseModel


class TagIn(TagModel):
    pass


class TagOut(TagModel, TagIDModel):
    pass
