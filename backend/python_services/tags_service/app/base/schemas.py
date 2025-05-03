from core.schemas import BaseModel, StrXSS, TagID
from pydantic import ConfigDict, Field, PositiveInt, AliasChoices
from typing import TypeAlias, Annotated
import annotated_types
import re


class TagIDModel(BaseModel):
    tag_id: TagID = Field(alias=AliasChoices('tag_id', 'id'))


class TagModel(BaseModel):
    name: str = Field(min_length=1, max_length=100, description='Unique tags name')
