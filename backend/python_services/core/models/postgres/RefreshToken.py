from sqlalchemy.orm import Mapped, mapped_column
from .Base import Base
from sqlalchemy import UUID, PrimaryKeyConstraint
from uuid import uuid4
from .User import UserDB
from .column_types import cascade_foreign_key, many_to_one_relationship, updated_at_type




class RefreshTokenDB(Base):
    
    __tablename__ = 'refresh_tokens'
    
    jti = mapped_column(UUID, default = uuid4)
    device_id = mapped_column(UUID)
    user_id : Mapped[int] = mapped_column(cascade_foreign_key('users.id'))
    subject : Mapped[UserDB] = many_to_one_relationship(back_populates = 'tokens')
    updated_at : Mapped[updated_at_type]
    
    __table_args__ = (PrimaryKeyConstraint('device_id', 'user_id'), )