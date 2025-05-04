from fastapi import APIRouter, Depends, Request
from core.dependencies.JWTToken import verify_user
from .errors import MeetingExeption
from .dependencies import get_meeting_members_dao, get_meeting_concatinate_dao, get_meeting_utils, MeetingUtils
from .dao import MeetingMembersDAO, MeetingConcatinateDAO
from .schemas import MeetingOut, MeetingIn, SuccessMeetingCreateOut, ChangeMeetingStatusIn
from core.schemas import UserActionOut
from app.notify import MeetingNotifyUtils, get_meeting_notify_utils


router = APIRouter(
                    prefix = '/my',
                    tags = ['Meetings'],
                    dependencies = [Depends(verify_user)],
                    responses = MeetingExeption.get_responses_schemas()
                )




@router.get(
                path = '',
                summary = 'Get your meetings'
            )
async def get_user_meetings(
                            request : Request,
                            dao : MeetingMembersDAO = Depends(get_meeting_members_dao),
                            meeting_utils : MeetingUtils = Depends(get_meeting_utils),
                        ) -> list[MeetingOut]:
    user_meetings = await dao.get_user_meetings(request.state.user.user_id)
    return meeting_utils.cast_meetings_to_response(user_meetings)



@router.post(
                path = '',
                summary = 'Create new meeting'
            )       
async def create_new_meeting(
                                request : Request,
                                form : MeetingIn,
                                dao : MeetingConcatinateDAO = Depends(get_meeting_concatinate_dao),
                                meeting_utils : MeetingUtils = Depends(get_meeting_utils),
                                notify_utils : MeetingNotifyUtils = Depends(get_meeting_notify_utils)
                            ) -> SuccessMeetingCreateOut:
    error = await meeting_utils.can_two_users_start_meeting(
                                                        request.state.user.user_id, 
                                                        form.meeting_user_id, 
                                                        form.meeting_datetime
                                                    )
    
    if error is not None:
        raise error 
    
    meeting_id, joined_users = await dao.create_new_meeting(
                                                        form.meeting_datetime.start, 
                                                        form.meeting_datetime.end,
                                                        [form.meeting_user_id, request.state.user.user_id]
                                                    )
    await notify_utils.new_meeting_notify(meeting_id, joined_users)
    return SuccessMeetingCreateOut(meeting_id = meeting_id)



@router.post(
                path = '/cancel',
                summary = 'Cancel your planned meeting'
            )
async def cancel_meeting(
                            request : Request,
                            form : ChangeMeetingStatusIn,
                            dao : MeetingConcatinateDAO = Depends(get_meeting_concatinate_dao),
                            notify_utils : MeetingNotifyUtils = Depends(get_meeting_notify_utils)
                        ) -> UserActionOut:
    await dao.cnacel_meeting_by_user(request.state.user.user_id, form.meeting_id)
    await notify_utils.cancel_meeting_notify(form.meeting_id)
    return UserActionOut()
    
    

@router.post(
                path = '/complete',
                summary = 'Complete your planned meeting'
            )
async def complete_meeting(
                            request : Request,
                            form : ChangeMeetingStatusIn,
                            dao : MeetingConcatinateDAO = Depends(get_meeting_concatinate_dao),
                            notify_utils : MeetingNotifyUtils = Depends(get_meeting_notify_utils)
                        ) -> UserActionOut:
    await dao.complete_meeting_by_user(request.state.user.user_id, form.meeting_id)
    await notify_utils.complete_meeting_notify(form.meeting_id)
    return UserActionOut()
    
    