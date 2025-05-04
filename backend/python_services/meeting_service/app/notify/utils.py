from core.models.rabbitmq.ban import UserBanNotify, UserBanNotifyType
from core.models.rabbitmq.meeting import MeetingNotify, NewMeetingNotify, MeetingStatusType
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from core.schemas import UserID, MeetingID
from core.utils import BaseNotifyUtils



class UserBanNotifyUtils(BaseNotifyUtils):
    
    
    __slots__ = ()
        
        
    async def user_ban_notify(self, blocker_user_id : UserID, blocked_user_id : UserID) -> None:
        await self.publisher.publish(
                                        UserBanNotify(
                                            status = UserBanNotifyType.BAN,
                                            blocked_user_id = blocked_user_id,
                                            blocker_user_id = blocker_user_id
                                        ),
                                        priority = 2
                                    )            
        
    async def user_unban_notify(self, blocker_user_id : UserID, blocked_user_id : UserID) -> None:
        await self.publisher.publish(
                                        UserBanNotify(
                                            status = UserBanNotifyType.UNBAN,
                                            blocked_user_id = blocked_user_id,
                                            blocker_user_id = blocker_user_id
                                        ),
                                        priority = 1
                                    )      
                   
                   


class MeetingNotifyUtils(BaseNotifyUtils):
    
    
    __slots__ = ()
    
    
    async def new_meeting_notify(self, meeting_id : MeetingID, joined_users : list[UserID]) -> None:
        await self.publisher.publish(
                                        NewMeetingNotify(meeting_id = meeting_id, members = joined_users),
                                        priority = 2
                                    )
        
    async def cancel_meeting_notify(self, meeting_id : MeetingID) -> None:
        await self.publisher.publish(
                                        MeetingNotify(meeting_id = meeting_id, status = MeetingStatusType.CANCEL),
                                        priority = 1
                                    )
        
        
    async def complete_meeting_notify(self, meeting_id : MeetingID) -> None:
        await self.publisher.publish(
                                        MeetingNotify(meeting_id = meeting_id, status = MeetingStatusType.COMPLETE),
                                        priority = 1
                                    )