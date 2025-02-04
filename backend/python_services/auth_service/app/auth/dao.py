from .schemas import UserRegistrationCredentialsIn, UserLoginCredentialsIn, UserChangePasswordIn
from core.models.postgres import UserDB
from fastapi import status
from core.schemas import UserID
from sqlalchemy import select, insert, update
from core.exception import BaseHTTPException, BaseHTTPExceptionModel
from core.dao.postgres import PostgresDAO, AsyncSession
from core.dao.http import HTTPRequest, HTTPResponseType
from sqlalchemy.exc import IntegrityError
from core.dependencies.JWTToken import IssuedJWTTokensOut
from .errors import EmailOccupiedError, InvalidPasswordError, InvalidEmailError
from core.services.jwttoken import get_jwt_service_settings, encoded_secret_key



class AuthDAO(PostgresDAO):
    
    @classmethod
    async def get_tokens(cls, user_id : UserID) -> IssuedJWTTokensOut:
        jwt_service_settings = get_jwt_service_settings()
        response = await HTTPRequest.post(   
                                            server = jwt_service_settings.JWT_SERVICE_NAME,
                                            port = jwt_service_settings.JWT_SERVICE_PORT,
                                            endpoint = jwt_service_settings.JWT_ISSUE_TOKENS_ENDPOINT,
                                            headers = {'SecretKey' : encoded_secret_key()},
                                            body = {'user_id' : user_id},
                                            response_method = HTTPResponseType.JSON
                                        )
        
        if response.get('detail') is not None:
            raise BaseHTTPException(
                                    status_code = status.HTTP_400_BAD_REQUEST,
                                    detail = BaseHTTPExceptionModel.model_validate(response['detail'])
                                )
        
        return IssuedJWTTokensOut.model_validate(response)  

    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def registrate(
                        cls,
                        session : AsyncSession, 
                        *,
                        user_credentials : UserRegistrationCredentialsIn
                    ) -> UserID:
        user_id : UserID
        query_for_new_user = insert(UserDB).values(user_credentials.model_dump()).returning(UserDB.id)
        
        try:
            user_id = await session.scalar(query_for_new_user)
        except IntegrityError:
            raise EmailOccupiedError
        
        return user_id
    
    
    @classmethod
    @PostgresDAO.get_session()
    async def login(
                    cls,
                    session : AsyncSession,
                    *,
                    user_credentials : UserLoginCredentialsIn
                ) -> UserID:
        user_data = user_credentials.model_dump()
        query_for_find_user = select(UserDB).where(UserDB.email == user_data['email'])
        user = await session.scalar(query_for_find_user)
        
        if user is None:
            raise InvalidEmailError
        
        if user.hash_password != user_data['hash_password']:
            raise InvalidPasswordError 
        
        return user.id
    
    
    @classmethod
    @PostgresDAO.get_session(auto_commit = True)
    async def change_password(
                                cls,
                                session : AsyncSession,
                                *,
                                user_credentials : UserChangePasswordIn
                            ) -> None:
        user_data = user_credentials.model_dump()
        query_for_update_password = update(UserDB).where(
                                                            UserDB.email == user_data['email']
                                                        ).values(
                                                            hash_password = user_data['hash_password']
                                                        ).returning(
                                                            UserDB.id
                                                        )
                        
        user_id = await session.scalar(query_for_update_password)
        
        if user_id is None:
            raise InvalidEmailError
        
        return user_id
        
        