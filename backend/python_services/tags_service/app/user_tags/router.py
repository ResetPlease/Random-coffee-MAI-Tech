from fastapi import APIRouter, Depends, Request
from core.dependencies.JWTToken import JWTException, verify_user
from .schemas import UserTagsListIn, TagID, UserTagOut, UserTagsChangeOut
from .dependencies import get_user_tags_dao
from .dao import UserTagsDAO
from core.models.postgres import TagDB
from app.notify import get_tags_notify_utils, UserTagsNotifyUtils


router = APIRouter(
                    prefix = '/my',
                    tags = ['User tags'],
                    responses = JWTException.get_responses_schemas(),
                    dependencies = [Depends(verify_user)],
                )


@router.get(path = '', description = 'Get all user tags')
async def get_user_tags(
                        request: Request, 
                        user_tags_dao: UserTagsDAO = Depends(get_user_tags_dao)
                    ) -> list[UserTagOut]:
    user_tags: list[TagDB] = await user_tags_dao.get_all_user_tags(request.state.user.user_id)
    return [UserTagOut.model_validate(tag) for tag in user_tags]


@router.post(path = '/add', description = 'Add new tags for user')
async def add_new_user_tags(
                            request: Request,
                            list_of_ids: UserTagsListIn,
                            user_tags_dao: UserTagsDAO = Depends(get_user_tags_dao),
                            notify_utils: UserTagsNotifyUtils = Depends(get_tags_notify_utils),
                        ) -> UserTagsChangeOut:
    user_added_tag_ids = await user_tags_dao.add_new_user_tags(request.state.user.user_id, list_of_ids.tag_ids)
    await notify_utils.tags_add_notify(request.state.user.user_id, user_added_tag_ids)
    return UserTagsChangeOut(changed_tag_ids = user_added_tag_ids)


@router.post(path = '/remove', description = 'Delete user tags for user')
async def delete_user_tags(
                        request: Request,
                        list_of_ids: UserTagsListIn,
                        user_tags_dao: UserTagsDAO = Depends(get_user_tags_dao),
                        notify_utils: UserTagsNotifyUtils = Depends(get_tags_notify_utils),
                    ) -> UserTagsChangeOut:
    user_deleted_tag_ids = await user_tags_dao.delete_user_tags(request.state.user.user_id, list_of_ids.tag_ids)
    await notify_utils.tags_remove_notify(request.state.user.user_id, user_deleted_tag_ids)
    return UserTagsChangeOut(changed_tag_ids = user_deleted_tag_ids)
