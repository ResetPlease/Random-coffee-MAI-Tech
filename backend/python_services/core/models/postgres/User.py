from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .column_types import pk_key_identity_column, unique_column, one_to_many_relationship
from enum import StrEnum, auto
from .Base import Base




class UserRoleType(StrEnum):
    user = auto()
    admin = auto()





class UserDB(Base):

    __tablename__ = 'users'
  
    id : Mapped[int] = pk_key_identity_column()
    role : Mapped[UserRoleType] = mapped_column(server_default = UserRoleType.user)
    first_name : Mapped[str] = mapped_column(String(50)) 
    last_name : Mapped[str] = mapped_column(String(50))
    email : Mapped[str] = unique_column(String(255))
    hash_password : Mapped[str] = mapped_column(String(64))
    
    tags = one_to_many_relationship('UserTagsDB', back_populates = 'user')
    meetings = one_to_many_relationship('MeetingMemberDB', back_populates = 'user')
