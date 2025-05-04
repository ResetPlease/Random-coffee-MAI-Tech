from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base
from sqlalchemy import PrimaryKeyConstraint
from .column_types import many_to_one_relationship, cascade_foreign_key
from . import UserDB
from .Tag import TagDB




class UserTagsDB(Base):
    __tablename__ = 'users_tags_association'
    
    user_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'))
    tag_id : Mapped[int] = mapped_column(cascade_foreign_key('tags.id'))
    
    user : Mapped[UserDB] = many_to_one_relationship(back_populates = 'tags')
    tag : Mapped[TagDB] = many_to_one_relationship(back_populates = 'users')
    
    __table_args__ = (PrimaryKeyConstraint('user_id', 'tag_id'), )
