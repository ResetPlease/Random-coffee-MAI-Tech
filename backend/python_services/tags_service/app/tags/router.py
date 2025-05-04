from fastapi import APIRouter, Depends, Request
from .dependencies import get_tag_dao
from .dao import TagDAO
from .schemas import TagOut


router = APIRouter(tags = ['Tags'])


@router.get(path = '', description = 'Get all tags')
async def get_user_tags(tag_dao: TagDAO = Depends(get_tag_dao)) -> list[TagOut]:
    tags = await tag_dao.get_all_tags()
    return [TagOut.model_validate(tag) for tag in tags]
