from core.models.postgres import RefreshTokenDB, UserDB
from core.dependencies.JWTToken import TokenRevokedError, IssuedJWTTokensOut, IssuedJWTTokenPayloadOut
from sqlalchemy import delete, insert, select, update
from .utils import JWTToken, TokenValidation
from core.dao.postgres import PostgresDAO, AsyncSession
from core.schemas import UserID, PublicUserInfoOut
from core.dao.redis import RedisDAO, Pipeline
from .JWTTokenType import JWTTokenType
from .config import jwtsettings
from .schemas import IssuedJWTTokensDataIn
from .errors import IncorrectUserIDError
from uuid import UUID
import asyncio




class JWTTokenDAO(PostgresDAO, RedisDAO):
    
    
    @classmethod
    async def set_access_token(
                                cls, 
                                pipeline : Pipeline,
                                user_id : UserID,
                                device_id : UUID,
                                jti : UUID
                            ) -> None:
        pipeline.multi()
        pipeline.set(f'{user_id}:{device_id}', f'{jti}', jwtsettings.ACCESS_TOKEN_TTL)
        await pipeline.execute()
     
    
    @classmethod
    async def delete_all_refresh_tokens(
                                        cls,
                                        session : AsyncSession,
                                        user_id : UserID
                                    ) -> list[UUID]:
        query_for_delete_all_tokens = delete(RefreshTokenDB).where(
                                                                RefreshTokenDB.user_id == user_id
                                                            ).returning(
                                                                RefreshTokenDB.device_id
                                                            )
        return await session.scalars(query_for_delete_all_tokens)
    
    
    @classmethod
    async def delete_all_access_tokens(
                                        cls, 
                                        pipeline : Pipeline,
                                        user_id : UserID,
                                        device_ids : list[UUID]
                                    ) -> None:
        pipeline.multi()
        pipeline.delete(*[f'{user_id}:{device_id}' for device_id in device_ids])
        await pipeline.execute()
        
        
    
    
    @classmethod
    @RedisDAO.get_pipeline()
    @PostgresDAO.get_session(auto_commit = True)
    async def issue_tokens(
                            cls, 
                            pipeline : Pipeline,
                            session : AsyncSession,
                            *, 
                            user_id : UserID
                        ) -> IssuedJWTTokensOut:
        query_for_select_user = select(UserDB).where(UserDB.id == user_id)
        user = await session.scalar(query_for_select_user)
        
        if user is None:
            raise IncorrectUserIDError
        
        tokens_data = IssuedJWTTokensDataIn(user_info = PublicUserInfoOut.model_validate(user))
        
        query_for_save_refresh_token = insert(RefreshTokenDB).values(
                                                                user_id = user_id,
                                                                device_id = tokens_data.device_id,
                                                                jti = tokens_data.jti_refresh_token
                                                            )

        await asyncio.gather(
                            session.execute(query_for_save_refresh_token),
                            cls.set_access_token(pipeline, user_id, tokens_data.device_id, tokens_data.jti_acsess_token)
                        )
        
        return JWTToken.generate_tokens(tokens_data)
        
        

    @classmethod
    @RedisDAO.get_pipeline()
    async def verify_access_token(
                                    cls, 
                                    pipeline : Pipeline,
                                    *,
                                    authorization_header : str
                                ) -> IssuedJWTTokenPayloadOut:
        payload = TokenValidation.get_token_payload(authorization_header, JWTTokenType.ACCESS)
        
        pipeline.multi()
        pipeline.get(f'{payload.user_id}:{payload.device_id}')
        response = await pipeline.execute()

        now_token_jti : bytes | None = response[0]
        
        if now_token_jti is None or UUID(now_token_jti.decode('utf-8')) != payload.jti:
            raise TokenRevokedError
        
        return payload
    
    
    @classmethod
    @RedisDAO.get_pipeline()
    @PostgresDAO.get_session(auto_commit = True, ignore_http_errors = True)
    async def update_tokens(
                            cls, 
                            pipeline : Pipeline,
                            session : AsyncSession,
                            *, 
                            refresh_token : str
                        ) -> IssuedJWTTokensOut:
        payload = TokenValidation.get_token_payload(refresh_token, JWTTokenType.REFRESH)
        new_tokens_data = IssuedJWTTokensDataIn(
                                            user_info = PublicUserInfoOut.model_validate(payload),
                                            device_id = payload.device_id
                                        )
        query_for_update_refresh_token = update(RefreshTokenDB).where(
                                                                    RefreshTokenDB.user_id == payload.user_id,
                                                                    RefreshTokenDB.device_id == payload.device_id,
                                                                    RefreshTokenDB.jti == payload.jti
                                                                ).values(
                                                                    jti = new_tokens_data.jti_refresh_token
                                                                ).returning(
                                                                    RefreshTokenDB.jti
                                                                )
        jti = await session.scalar(query_for_update_refresh_token)
        
        if jti is None:
            device_ids = await cls.delete_all_refresh_tokens(session, payload.user_id)
            await cls.delete_all_access_tokens(pipeline, payload.user_id, device_ids)
            raise TokenRevokedError
        
        await cls.set_access_token(pipeline, payload.user_id, payload.device_id, new_tokens_data.jti_acsess_token)
        
        return JWTToken.generate_tokens(new_tokens_data)
        
        
        
    
        
    
        
        
             
            