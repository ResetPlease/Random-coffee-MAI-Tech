from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import PrimaryKeyConstraint, CheckConstraint
from .column_types import cascade_foreign_key
from .Base import Base






class UserBanListDB(Base):
    
    __tablename__ = 'user_ban_list'
    
    blocker_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'))
    blocked_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'))
    
    __table_args__ = (PrimaryKeyConstraint('blocker_id', 'blocked_id'), CheckConstraint('blocker_id != blocked_id'))