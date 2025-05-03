from core.models.postgres import UserBanListDB, UserDB
from core.dao.postgres import PostgresDAO, AsyncSession
from core.schemas import UserID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError
from .errors import IncorrectUserIDError, YourselfBannedError
import logging




class UserBanListDAO(PostgresDAO):
    
    
    @PostgresDAO.get_session(auto_commit = True)
    async def block_user(
                            session : AsyncSession,
                            blocker_id : UserID,
                            blocked_id : UserID
                        ) -> bool:
        query_for_insert_block = insert(UserBanListDB).on_conflict_do_nothing().values(
                                                                                blocker_id = blocker_id,
                                                                                blocked_id = blocked_id
                                                                            ).returning(
                                                                                UserBanListDB.blocked_id
                                                                            )
        try:
            is_banned = await session.scalar(query_for_insert_block)
        except IntegrityError as error:
            match error.orig.sqlstate:
                case '23503':
                    raise IncorrectUserIDError
                case '23514':
                    raise YourselfBannedError
        
        return is_banned is not None
            
        
    
    @PostgresDAO.get_session()
    async def get_user_blocks(
                                session : AsyncSession,
                                user_id : UserID
                            ) -> list[UserDB]:
        query_for_select_user_blocks = select(UserDB).where(
                                    UserDB.id.in_(
                                                select(UserBanListDB.blocked_id).where(UserBanListDB.blocker_id == user_id)
                                            )
                                        )
        
        return await session.scalars(query_for_select_user_blocks)
    
    
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_user_block(
                                session : AsyncSession,
                                blocker_id : UserID,
                                blocked_id : UserID
                            ) -> bool:
        query_for_delete_user_block = delete(UserBanListDB).where(
                                                            UserBanListDB.blocker_id == blocker_id,
                                                            UserBanListDB.blocked_id == blocked_id
                                                        ).returning(
                                                            UserBanListDB.blocked_id
                                                        )
        
        is_unbanned = await session.scalar(query_for_delete_user_block)
        
        return is_unbanned is not None
        

    

    
    
    
    