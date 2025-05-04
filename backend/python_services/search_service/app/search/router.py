from fastapi import APIRouter, Depends, Request, Query
from core.dependencies.JWTToken import verify_user
from .schemas import MatchUserOut, SearchIn, UsersMatchingIn
from .dao import UsersSearchDAO
from app.base import UsersDAO, get_users_dao, IncorrectUserIDError
from .utils import SearchUtils
from .dependencies import get_users_search_dao, get_search_utils
from .errors import MatchException
from core.schemas import UserActionOut
import asyncio



router = APIRouter(
                    prefix = '',
                    tags = ['Search'],
                    responses = MatchException.get_responses_schemas()
                )




@router.get(
                path = '',
                summary = 'Get matched users',
                dependencies = [Depends(verify_user)]
            )
async def search_match_for_user(
                                request : Request,
                                form : SearchIn = Query(),
                                users_dao : UsersDAO = Depends(get_users_dao),
                                search_dao : UsersSearchDAO = Depends(get_users_search_dao),
                                search_utils : SearchUtils = Depends(get_search_utils)
                            ) -> list[MatchUserOut]:
    user = await users_dao.get_user_by_id(request.state.user.user_id)
    
    if user is None:
        raise IncorrectUserIDError
    
    skip, limit = search_utils.convert_page_to_skip_and_limit(form.page)
    matched_users = await search_dao.search_users_by_params(
                                                            user, 
                                                            form.only_new_users,
                                                            form.min_tags_match,
                                                            form.date_start,
                                                            form.date_end, 
                                                            form.time_start,
                                                            form.time_end,
                                                            skip,
                                                            limit
                                                        )
    return [MatchUserOut.model_validate(matched_user) for matched_user in matched_users]



@router.post(
                path = '/can-start-meeting',
                summary = 'Are these two users matched'
            )
async def can_start_meeting(
                            form : UsersMatchingIn,
                            users_dao : UsersDAO = Depends(get_users_dao),
                            search_utils : SearchUtils = Depends(get_search_utils)
                        ) -> UserActionOut:
    searcher_user, active_user = await asyncio.gather(
                                                        users_dao.get_user_by_id(form.searcher_user_id),
                                                        users_dao.get_searched_user_by_id(form.active_user_id)
                                                    )
    error = search_utils.is_two_users_can_start_meeting(searcher_user, active_user, form.meeting_datetime.start, form.meeting_datetime.end)
    if error is not None:
        raise error
    return UserActionOut()
    
    

