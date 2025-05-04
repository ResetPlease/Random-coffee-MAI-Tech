from core.dao.postgres import PostgresDAO, AsyncSession
from core.param_decorator import class_parameter
from core.models.postgres import TagDB, UserTagsDB
from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from core.schemas import UserID
from typing import Iterable
from app.base import TagID
from sqlalchemy.exc import IntegrityError
from .errors import IncorrectTagIDError


class UserTagsDAO(PostgresDAO):

    @class_parameter()
    @PostgresDAO.get_session()
    async def get_all_user_tags(self, user_id: UserID, session: AsyncSession) -> list[TagDB]:

        query_for_select_user_tags = select(TagDB).where(
            TagDB.id.in_(select(UserTagsDB.tag_id).where(UserTagsDB.user_id == user_id))
        )
        user_tags = await session.scalars(query_for_select_user_tags)
        return user_tags



    @class_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def add_new_user_tags(self, session: AsyncSession, user_id: UserID, list_of_id: list[TagID]) -> list[TagID]:
        list_of_id.sort()
        query_for_add_new_user_tags = (
            insert(UserTagsDB)
            .on_conflict_do_nothing()
            .values([{'user_id': user_id, 'tag_id': tag_id} for tag_id in list_of_id])
            .returning(UserTagsDB.tag_id)
        )
        try:
            added_tag_ids = await session.scalars(query_for_add_new_user_tags)
        except IntegrityError:
            raise IncorrectTagIDError

        return added_tag_ids.all()

    @class_parameter()
    @PostgresDAO.get_session(auto_commit = True)
    async def delete_user_tags(self, session: AsyncSession, user_id: UserID, list_of_id: list[TagID]) -> list[TagID]:
        list_of_id.sort()
        query_for_delete_user_tags = (
            delete(UserTagsDB)
            .where(UserTagsDB.user_id == user_id, UserTagsDB.tag_id.in_(list_of_id))
            .returning(UserTagsDB.tag_id)
        )

        deleted_tag_ids = await session.scalars(query_for_delete_user_tags)

        return deleted_tag_ids.all()
