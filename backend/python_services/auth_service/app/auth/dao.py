from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, UserChangePasswordIn
from core.schemas import UserID
from sqlalchemy import select, insert, update
from core.dao.postgres import PostgresDAO, AsyncSession
from core.param_decorator import self_parameter
from sqlalchemy.exc import IntegrityError
from .errors import EmailOccupiedError, InvalidPasswordError, InvalidEmailError
from .utils import AuthenticationUtils
from pydantic import EmailStr
from core.models.postgres import UserDB




class AuthenticationDAO(PostgresDAO):
    
    
    __slots__ = ('auth_utils', )
    
    
    def __init__(self, auth_utils : AuthenticationUtils) -> None:
        self.auth_utils = auth_utils

    
    
    @self_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def create_new_user(
                            self,
                            session : AsyncSession, 
                            user_credentials : UserRegistrationCredentialsIn
                        ) -> UserID:
        user_id : UserID
        query_for_new_user = insert(UserDB).values(
                                                    hash_password = self.auth_utils.hashing_password(user_credentials.password),
                                                    **user_credentials.model_dump()
                                                ).returning(
                                                    UserDB.id
                                                )
        
        try:
            user_id = await session.scalar(query_for_new_user)
        except IntegrityError:
            raise EmailOccupiedError
        
        return user_id
    
    
    
    @self_parameter()
    @PostgresDAO.get_session()
    async def get_user_by_email(
                                self,
                                session : AsyncSession,
                                email : EmailStr,
                                password : str
                            ) -> UserDB:
        query_for_find_user = select(UserDB).where(UserDB.email == email)
        user = await session.scalar(query_for_find_user)
        
        if user is None:
            raise InvalidEmailError
        
        if user.hash_password != self.auth_utils.hashing_password(password):
            raise InvalidPasswordError 
        
        return user
    
    
    
    @self_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def change_user_password(
                                    self,
                                    session : AsyncSession,
                                    email : EmailStr,
                                    new_password : str
                                ) -> None:
        query_for_update_password = update(UserDB).where(
                                                        UserDB.email == email
                                                    ).values(
                                                        hash_password = self.auth_utils.hashing_password(new_password)
                                                    ).returning(
                                                        UserDB.id
                                                    )
                        
        user_id = await session.scalar(query_for_update_password)
        
        if user_id is None:
            raise InvalidEmailError




