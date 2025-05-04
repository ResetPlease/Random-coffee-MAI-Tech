from core.models.postgres import MeetingMemberDB, MeetingDB, UserDB, MeetingStatusType
from core.param_decorator import class_parameter, self_parameter
from core.dao.postgres import PostgresDAO, AsyncSession
from datetime import datetime
from .schemas import MeetingID
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import selectinload, joinedload
from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError
from .errors import (
                        IncorrectMeetingDatetimeError, 
                        IncorrectUserIDError,
                        UserAlreadyHasMettingError,
                        CanceledMeetingError,
                        CompletedMeetingError,
                        MemberMeetingError
                    )
from core.schemas import UserID
import logging




class MeetingDAO(PostgresDAO):
    
    
    @class_parameter()
    async def create_new_meeting(
                                cls,
                                session : AsyncSession, 
                                meeting_datetime_start : datetime,
                                meeting_datetime_end : datetime
                            ) -> MeetingID:
        query_for_insert_meeting = insert(MeetingDB).values(
                                                        meeting_datetime_start = meeting_datetime_start,
                                                        meeting_datetime_end = meeting_datetime_end
                                                    ).returning(
                                                        MeetingDB.id
                                                    )
        try:
            meeting_id = await session.scalar(query_for_insert_meeting)
        except IntegrityError:
            raise IncorrectMeetingDatetimeError
        return meeting_id
    
    
    @class_parameter()
    async def _change_meeting_status(cls, session : AsyncSession, meeting_id : MeetingID, status : MeetingStatusType) -> bool:
        query_for_cancel_meeting = update(MeetingDB).where(
                                                            MeetingDB.id == meeting_id,
                                                            MeetingDB.status == MeetingStatusType.planned
                                                        ).values(
                                                            status = status
                                                        ).returning(
                                                            MeetingDB.id
                                                        )
        
        is_chaged = await session.scalar(query_for_cancel_meeting)
        return is_chaged is not None
    
    
    
    @class_parameter()
    async def cancel_meeting(cls, session : AsyncSession, meeting_id : MeetingID) -> None:
        is_chaged = await cls._change_meeting_status(session, meeting_id, MeetingStatusType.canceled)

        if not is_chaged:
            raise CanceledMeetingError
        
        
    
    @class_parameter()
    async def complete_meeting(cls, session : AsyncSession, meeting_id : MeetingID) -> None:
        is_chaged = await cls._change_meeting_status(session, meeting_id, MeetingStatusType.completed)

        if not is_chaged:
            raise CompletedMeetingError
    
        
        
            
    
    
    

class MeetingMembersDAO(PostgresDAO):
    
    
    @class_parameter()
    async def does_users_have_meeting_at_this_time(
                                                    cls,
                                                    session : AsyncSession,
                                                    meeting_datetime_start : datetime,
                                                    meeting_datetime_end : datetime,
                                                    list_of_ids : list[UserID]
                                                ) -> bool:
        query_for_check_users_meetings = select(MeetingDB.id).where(
                                                                MeetingDB.meeting_datetime_start < meeting_datetime_end,
                                                                MeetingDB.meeting_datetime_end > meeting_datetime_start,
                                                                MeetingDB.status == MeetingStatusType.planned,
                                                                MeetingDB.id.in_(
                                                                        select(MeetingMemberDB.meeting_id).where(
                                                                                    MeetingMemberDB.user_id.in_(list_of_ids)
                                                                    )
                                                                )
                                                            ).limit(1)
        is_exist = await session.scalar(query_for_check_users_meetings)
        return is_exist is not None



    
    @class_parameter()
    async def attach_users_to_meeting(
                                        cls,
                                        session : AsyncSession,
                                        meeting_id : MeetingID,
                                        list_of_ids : list[UserID]
                                    ) -> list[UserID]:
        list_of_ids.sort()
        query_for_join_users_to_meeting = insert(MeetingMemberDB).on_conflict_do_nothing().values(
                                                                        [
                                                                            {'meeting_id' : meeting_id, 'user_id' : user_id}
                                                                            for user_id in list_of_ids
                                                                        ]
                                                                    ).returning(
                                                                        MeetingMemberDB.user_id
                                                                    )
        try:
            joined_ids = await session.scalars(query_for_join_users_to_meeting)
        except IntegrityError:
            raise IncorrectUserIDError
        return joined_ids.all()
    
    
    
    
    @class_parameter()
    @PostgresDAO.get_session()
    async def get_user_meetings(
                                cls,
                                session : AsyncSession, 
                                user_id : UserID
                            ) -> list[MeetingDB]:
        
        query_for_select_user_meetings = select(MeetingDB).options(
                                                                    selectinload(
                                                                            MeetingDB.members.and_(
                                                                                        MeetingMemberDB.user_id != user_id
                                                                                    )
                                                                        ).options(
                                                                            selectinload(
                                                                                    MeetingMemberDB.user
                                                                                )
                                                                        )
                                                                ).where(
                                                                    MeetingDB.id.in_(
                                                                            select(MeetingMemberDB.meeting_id).where(
                                                                                        MeetingMemberDB.user_id == user_id
                                                                            )
                                                                        )
                                                                ).order_by(
                                                                    MeetingDB.status,
                                                                    MeetingDB.id.desc()
                                                                )
                                                                
        user_meetings = await session.scalars(query_for_select_user_meetings)
        
        return user_meetings.all()
        
        
        
    
    @class_parameter()
    async def user_is_attached_to_meeting(
                                            cls,
                                            session : AsyncSession,
                                            user_id : UserID,
                                            meeting_id : MeetingID
                                        ) -> bool:
        query_for_check_user_in_meeting = select(MeetingMemberDB.user_id).where(
                                                                            MeetingMemberDB.user_id == user_id,
                                                                            MeetingMemberDB.meeting_id == meeting_id
                                                                        )
        is_attached = await session.scalar(query_for_check_user_in_meeting)
        return is_attached is not None






class MeetingConcatinateDAO(PostgresDAO):
    
    __slots__ = ('meeting_dao', 'meeting_members_dao')
    
    def __init__(self, meeting_dao : MeetingDAO, meeting_members_dao : MeetingMembersDAO) -> None:
        self.meeting_dao = meeting_dao
        self.meeting_members_dao = meeting_members_dao
        
        
    @self_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def create_new_meeting(
                                self,
                                session : AsyncSession, 
                                meeting_datetime_start : datetime,
                                meeting_datetime_end : datetime,
                                meeting_users : list[UserID]
                            ) -> tuple[MeetingID, list[UserID]]:
        have_any_user_meeting = await self.meeting_members_dao.does_users_have_meeting_at_this_time(session, meeting_datetime_start, meeting_datetime_end, meeting_users)
        
        if have_any_user_meeting:
            raise UserAlreadyHasMettingError
        
        meeting_id = await self.meeting_dao.create_new_meeting(session, meeting_datetime_start, meeting_datetime_end)
        joined_users = await self.meeting_members_dao.attach_users_to_meeting(session, meeting_id, meeting_users)
        return meeting_id, joined_users
    
    
    
    @self_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def cnacel_meeting_by_user(
                                    self,
                                    session : AsyncSession,
                                    user_who_changed : UserID,
                                    meeting_id : MeetingID
                                ) -> None:
        user_in_meeting = await self.meeting_members_dao.user_is_attached_to_meeting(session, user_who_changed, meeting_id)
        
        if not user_in_meeting:
            raise MemberMeetingError
        
        await self.meeting_dao.cancel_meeting(session, meeting_id)
        
        
    @self_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def complete_meeting_by_user(
                                        self,
                                        session : AsyncSession,
                                        user_who_changed : UserID,
                                        meeting_id : MeetingID
                                    ) -> None:
        user_in_meeting = await self.meeting_members_dao.user_is_attached_to_meeting(session, user_who_changed, meeting_id)
        
        if not user_in_meeting:
            raise MemberMeetingError
        
        await self.meeting_dao.complete_meeting(session, meeting_id)
        
    
    