from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncAttrs
from sqlalchemy.orm import DeclarativeBase, sessionmaker
from .config import get_db_url


DATABASE_URL = get_db_url()
engine = create_async_engine(DATABASE_URL, echo = True) 
sync_session_maker = sessionmaker()
async_session_maker = async_sessionmaker(engine, sync_session_class = sync_session_maker)



class Base(AsyncAttrs, DeclarativeBase):
    
    __abstract__ = True
    
    
    def __repr__(self) -> str:
        name : str = self.__class__.__name__
        str_attrs : list[str] = []
        
        for attr, value in self.__dict__.items():
            if attr.startswith('_') is not True and hasattr(value, '__repr__') is True:
                str_attrs.append(f'{attr} = {value}')
                
        return f'{name}({", ".join(str_attrs)})'
    
    
