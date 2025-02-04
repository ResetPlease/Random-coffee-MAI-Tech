from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String
from .Base import Base
from .column_types import pk_key_identity_column, unique_column, one_to_many_relationship, many_to_many_relationship



class UserDB(Base):

    __tablename__ = 'users'
  
    id : Mapped[int] = pk_key_identity_column()
    first_name : Mapped[str] = mapped_column(String(50)) 
    last_name : Mapped[str] = mapped_column(String(50))
    email : Mapped[str] = unique_column(String(255))
    hash_password : Mapped[str] = mapped_column(String(64))
  
    tokens = one_to_many_relationship('RefreshTokenDB', back_populates = 'subject')