from core.schemas import UserID, TagID
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from .dao import NewUserDAO
from core.models.rabbitmq.tags import ChangeUserTagsNotify, TagsChangeNotifyType
from core.utils import BaseNotifyUtils


class UserTagsNotifyUtils(BaseNotifyUtils):

    __slots__ = ('new_users_dao', )

    def __init__(self, publisher: AsyncAPIPublisher, new_users_dao: NewUserDAO) -> None:
        self.publisher = publisher
        self.new_users_dao = new_users_dao



    async def tags_add_notify(self, user_id: UserID, tag_ids: list[TagID]) -> None:
        if not tag_ids:
            return

        form = ChangeUserTagsNotify(
            status = TagsChangeNotifyType.ADD, user_id = user_id, tag_ids = tag_ids
        )

        if not await self.new_users_dao.is_new_user(user_id):
            await self.publisher.publish(form, priority = 2)
            return

        await self.publisher.publish(form, priority = 3)
        await self.new_users_dao.remove_new_user(user_id)


    async def tags_remove_notify(self, user_id: UserID, tag_ids: list[TagID]) -> None:
        if not tag_ids:
            return

        form = ChangeUserTagsNotify(
            status = TagsChangeNotifyType.DELETE, user_id = user_id, tag_ids = tag_ids
        )
        await self.publisher.publish(form, priority = 1)
