from sqlalchemy.orm import Mapped, mapped_column
from .column_types import pk_key_identity_column, created_at_type, one_to_many_relationship
from enum import StrEnum, auto
from .Base import Base
from datetime import datetime
from sqlalchemy import CheckConstraint



class MeetingStatusType(StrEnum):
    planned = auto()
    canceled = auto()
    completed = auto()
    



class MeetingDB(Base):
    
    __tablename__ = 'meetings'
    
    id : Mapped[int] = pk_key_identity_column()
    status : Mapped[MeetingStatusType] = mapped_column(server_default = MeetingStatusType.planned)
    meeting_datetime_start : Mapped[datetime]
    meeting_datetime_end : Mapped[datetime]
    created_at : Mapped[created_at_type]
    members = one_to_many_relationship('MeetingMemberDB', back_populates = 'meeting')
    
    __table_args__ = (
                        CheckConstraint('meeting_datetime_start > created_at'),
                        CheckConstraint('meeting_datetime_start < meeting_datetime_end')
                    )