from sqlalchemy.orm import Mapped
from sqlalchemy import String
from .Base import Base
from .column_types import many_to_one_relationship, unique_column, pk_key_column





class TagDB(Base):
    
    __tablename__ = 'tags'
    
    id : Mapped[int] = pk_key_column()
    name : Mapped[str] = unique_column(String(100))
    
    users = many_to_one_relationship('UserTagsDB', back_populates = 'tag')
    
    
    