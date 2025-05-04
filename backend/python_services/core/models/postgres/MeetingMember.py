from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, PrimaryKeyConstraint
from .column_types import many_to_one_relationship, created_at_type, cascade_foreign_key, unique_column
from enum import StrEnum, auto
from .Base import Base
from datetime import datetime




class MeetingMemberDB(Base):
    
    __tablename__ = 'meeting_members'
    meeting_id : Mapped[int] = mapped_column(cascade_foreign_key('meetings.id'), index = True)
    user_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'), index = True)
    joined_at : Mapped[created_at_type]
    
    meeting = many_to_one_relationship('MeetingDB', back_populates = 'members')
    user = many_to_one_relationship('UserDB', back_populates = 'meetings')
    
    __table_args__ = (PrimaryKeyConstraint('user_id', 'meeting_id'), )
    
    
    
    