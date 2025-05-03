from fastapi import APIRouter, Depends, Request, Path
from .dao import UserBanListDAO
from .dependencies import get_user_banlist_dao
from .schemas import UserBlockingIn
from core.dependencies.JWTToken import verify_user
from core.schemas import UserActionOut, PublicUserInfoOut
from .errors import UserBanExeption
from app.notify import UserBanNotifyUtils, get_user_ban_notify_utils



router = APIRouter(
                    prefix = '/ban-user/my',
                    tags = ['Users ban'],
                    dependencies = [Depends(verify_user)],
                    responses = UserBanExeption.get_responses_schemas()
                )




@router.get(
                path = '',
                summary = 'Get your users ban'
            )
async def get_user_banlist(
                            request : Request,
                            dao : UserBanListDAO = Depends(get_user_banlist_dao)
                        ) -> list[PublicUserInfoOut]:
    blocked_users = await dao.get_user_blocks(request.state.user.user_id)
    return [PublicUserInfoOut.model_validate(user) for user in blocked_users]




@router.post(
            path = '/ban',
            summary = 'Ban user'
        )
async def ban_user_by_id( 
                            request : Request,
                            form : UserBlockingIn,
                            dao : UserBanListDAO = Depends(get_user_banlist_dao),
                            notify_utils : UserBanNotifyUtils = Depends(get_user_ban_notify_utils)
                        ) -> UserActionOut:
    is_banned = await dao.block_user(request.state.user.user_id, form.blocked_id)
    if is_banned:
        await notify_utils.user_ban_notify(request.state.user.user_id, form.blocked_id)
    return UserActionOut()



@router.post(
            path = '/unban',
            summary = 'Unban user'
        )
async def unban_user_by_id( 
                            request : Request,
                            form : UserBlockingIn,
                            dao : UserBanListDAO = Depends(get_user_banlist_dao),
                            notify_utils : UserBanNotifyUtils = Depends(get_user_ban_notify_utils)
                        ) -> UserActionOut:
    is_unbanned = await dao.delete_user_block(request.state.user.user_id, form.blocked_id)
    if is_unbanned:
        await notify_utils.user_unban_notify(request.state.user.user_id, form.blocked_id)
    return UserActionOut()