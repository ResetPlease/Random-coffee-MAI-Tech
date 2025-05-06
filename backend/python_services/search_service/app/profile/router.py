from fastapi import APIRouter, Depends, Request, Query
from core.dependencies.JWTToken import verify_user
from app.base import UsersDAO, get_users_dao, IncorrectUserIDError, ActiveSearchUserOut
from core.schemas import UserActionOut
from .schemas import SearchUserProfileOut, SearchUserProfileIn
from .dao import SearchProfileDAO
from .dependencies import get_search_profile_dao
from .errors import SearchProfileException




router = APIRouter(
                    prefix = '/profile/my',
                    tags = ['Search profile'],
                    dependencies = [Depends(verify_user)],
                    responses = SearchProfileException.get_responses_schemas()
                )




@router.get(
            path = '',
            summary = 'Get user search profile'
        )
async def get_user_search_profile_information(
                                                request : Request,
                                                users_dao : UsersDAO = Depends(get_users_dao),
                                            ) -> SearchUserProfileOut:
    user = await users_dao.get_searched_user_by_id(request.state.user.user_id)
    return SearchUserProfileOut(information = user)




@router.post(
                path = '',
                summary = 'Create or update user search profile'
        )
async def create_or_update_user_search_profile(
                                                request : Request,
                                                form : SearchUserProfileIn,
                                                search_profile_dao : SearchProfileDAO = Depends(get_search_profile_dao)
                                            ) -> UserActionOut:
    if not form.meeting_intervals:
        await search_profile_dao.delete_user_profile(request.state.user.user_id)
    else:
        await search_profile_dao.create_or_update_user_profile(request.state.user.user_id, form.min_tags_match, form.meeting_intervals)
    return UserActionOut()




@router.post(
                path = '/delete',
                summary = 'Delete user search profile'
        )
async def delete_user_search_profile(
                                    request : Request,
                                    search_profile_dao : SearchProfileDAO = Depends(get_search_profile_dao)
                                ) -> UserActionOut:
    await search_profile_dao.delete_user_profile(request.state.user.user_id)
    return UserActionOut()