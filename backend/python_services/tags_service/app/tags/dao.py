from core.dao.postgres import PostgresDAO, AsyncSession
from core.param_decorator import self_parameter
from core.models.postgres import TagDB
from sqlalchemy import select


class TagDAO(PostgresDAO):

    def __init__(self) -> None:
        pass

    @self_parameter()
    @PostgresDAO.get_session()
    async def get_all_tags(self, session: AsyncSession) -> list[TagDB]:
        query_for_select_all_tags = select(TagDB)
        return await session.scalars(query_for_select_all_tags)
