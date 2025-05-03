from core.models.rabbitmq import rabbitmq_router
from core.models.rabbitmq.user import get_create_user_subscriber, CreateUserNotify
from core.models.rabbitmq.tags import get_tags_subscriber, TagsChangeNotifyType, ChangeUserTagsNotify
from core.models.rabbitmq.ban import get_ban_subscriber, UserBanNotifyType, UserBanNotify
from core.models.rabbitmq.meeting import get_meeting_subscriber, NewMeetingNotify, MeetingNotify, MeetingStatusType
from fastapi import Depends
from .dependencies import get_change_users_dao, get_update_users_utils, get_meeting_dao, get_user_meeting_concatinate_dao
from .dao import UpdateUsersDAO, MeetingsDAO, UsersMeetingConcatinateDAO
from .utils import UpdateUsersUtils
from faststream.exceptions import NackMessage
import asyncio
import logging




@get_create_user_subscriber('search_service.create_user')
async def create_new_user(
                        form : CreateUserNotify,
                        users_dao : UpdateUsersDAO = Depends(get_change_users_dao),
                    ) -> None:
    await users_dao.create_new_user(form.user_id, form.first_name, form.last_name, form.email)
    
    
    
@get_tags_subscriber('search_service.tags')
async def update_user_tags(
                            form : ChangeUserTagsNotify,
                            users_dao : UpdateUsersDAO = Depends(get_change_users_dao),
                            users_utils : UpdateUsersUtils = Depends(get_update_users_utils)
                        ) -> None:
    is_update = False
    if form.status == TagsChangeNotifyType.ADD:
        is_update = await users_dao.add_user_tag_ids(form.user_id, form.tag_ids)
        
    elif form.status == TagsChangeNotifyType.DELETE:
        is_update = await users_dao.remove_user_tag_ids(form.user_id, form.tag_ids)    
    
    if not is_update:
        await asyncio.sleep(users_utils.nack_message_block_seconds)
        raise NackMessage()
    
    
    
@get_ban_subscriber('search_service.ban')
async def update_ban_users_list(
                                form : UserBanNotify,
                                users_dao : UpdateUsersDAO = Depends(get_change_users_dao),
                                users_utils : UpdateUsersUtils = Depends(get_update_users_utils)
                            ) -> None:
    is_update = False
    if form.status == UserBanNotifyType.BAN:
        is_update = await users_dao.add_banned_user_id(form.blocker_user_id, [form.blocked_user_id])    
    else:
        is_update = await users_dao.remove_banned_user_ids(form.blocker_user_id, [form.blocked_user_id])    
    
    if not is_update:
        await asyncio.sleep(users_utils.nack_message_block_seconds)
        raise NackMessage()
    
    
    
    
@get_meeting_subscriber('search_service.meeting')
async def update_users_meetings(
                                form : NewMeetingNotify | MeetingNotify,
                                dao : UsersMeetingConcatinateDAO = Depends(get_user_meeting_concatinate_dao),
                                users_utils : UpdateUsersUtils = Depends(get_update_users_utils)
                            ) -> None:
    is_update = False
    if isinstance(form, NewMeetingNotify):
        is_update = await dao.create_new_meeting(form.meeting_id, form.members)
        
    elif isinstance(form, MeetingNotify):
        if form.status == MeetingStatusType.CANCEL:
            is_update = await dao.cancel_meeting(form.meeting_id)
        elif form.status == MeetingStatusType.COMPLETE:
            is_update = await dao.complete_meeting(form.meeting_id)
    
    if not is_update:
        await asyncio.sleep(users_utils.nack_message_block_seconds)
        raise NackMessage()
    
    
        

        
    
    
