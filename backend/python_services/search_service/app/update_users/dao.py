from core.dao.mongo import MongoDAO, AsyncCollection
from core.schemas import TagID, UserID, MeetingID
from pydantic import EmailStr
from typing import Any
from core.param_decorator import class_parameter, self_parameter
from pymongo import UpdateOne
from app.profile.dao import SearchProfileDAO
import logging



class MeetingsDAO(MongoDAO):
    
    @MongoDAO.get_collection('meetings')
    async def create_new_meeting(
                                collection : AsyncCollection, 
                                meeting_id : MeetingID,
                                members : list[UserID]
                            ) -> None:
        await collection.insert_one(
                                    {
                                        '_id' : meeting_id,
                                        'user_ids' : members
                                    }       
                                )
        
    @MongoDAO.get_collection('meetings')
    async def delete_meeting(
                                collection : AsyncCollection, 
                                meeting_id : MeetingID,
                            ) -> list[UserID] | None:
        meeting = await collection.find_one_and_delete({'_id' : meeting_id})
        return meeting['user_ids'] if meeting is not None else None
    





class UpdateUsersDAO(MongoDAO):
    
    
    
    @MongoDAO.get_collection('users')
    async def create_new_user(
                            collection : AsyncCollection, 
                            user_id : UserID, 
                            first_name : str,
                            last_name : str, 
                            email : EmailStr
                        ) -> None:
        await collection.insert_one(
                                        {
                                           '_id' : user_id,
                                           'first_name' : first_name, 
                                           'last_name' : last_name,
                                           'email' : email,
                                           'banned_user_ids' : [user_id],
                                           'tag_ids' : [],
                                           'completed_user_ids' : [],
                                           'planned_user_ids' : [],
                                           'is_search' : False
                                       }      
                                    )
        
    @staticmethod  
    async def add_new_values_to_user_array_field(
                                                    collection : AsyncCollection,
                                                    user_id : UserID,
                                                    field : str,
                                                    values : list[Any]
                                                ) -> bool:
        result = await collection.update_one(    
                                            {'_id' : user_id},
                                            {'$push' : {field : {'$each' : values}}}
                                        )
        return result.modified_count
    
    
    
    @staticmethod
    async def remove_values_from_user_array_field(
                                                    collection : AsyncCollection,
                                                    user_id : UserID,
                                                    field : str,
                                                    values : list[Any]
                                                ) -> bool:
        result = await collection.update_one(    
                                            {
                                                '_id' : user_id,
                                                field : {'$all' : values}
                                            },
                                            {'$pull' : {field : {'$in' : values}}}
                                        )
        return result.matched_count
        
        
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def add_user_tag_ids(cls, collection : AsyncCollection, user_id : UserID, tag_ids : list[TagID]) -> bool:
        return await cls.add_new_values_to_user_array_field(collection, user_id, 'tag_ids', tag_ids)
        
        
        
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def remove_user_tag_ids(cls, collection : AsyncCollection, user_id : UserID, tag_ids : list[TagID]) -> bool:
        return await cls.remove_values_from_user_array_field(collection, user_id, 'tag_ids', tag_ids)
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def add_banned_user_id(
                                    cls, 
                                    collection : AsyncCollection,
                                    user_id : UserID, 
                                    banned_user_ids : list[UserID]
                                ) -> bool:
        return await cls.add_new_values_to_user_array_field(collection, user_id, 'banned_user_ids', banned_user_ids)
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def remove_banned_user_ids(
                                    cls, 
                                    collection : AsyncCollection, 
                                    user_id : UserID, 
                                    banned_user_ids : list[UserID]
                                ) -> bool:
        return await cls.remove_values_from_user_array_field(collection, user_id, 'banned_user_ids', banned_user_ids)
    
    
    @MongoDAO.get_collection('users')
    async def check_all_users_exist(
                                        collection : AsyncCollection, 
                                        user_ids : list[UserID]
                                    ) -> bool:
        all_users = collection.find({'_id' : {'$in' : user_ids}})
        users_list = await all_users.to_list()

        return len(users_list) == len(user_ids)
    
    
    @staticmethod
    def _get_bulk_operation_for_add_new_planned_meeting(user_ids : list[UserID]) -> list[UpdateOne]:
        bulk_operations : list[UpdateOne] = []
        for user_id in user_ids:
            bulk_operations.append(
                UpdateOne(
                    {'_id' : user_id},
                    {
                        '$push' : {'planned_user_ids' : {'$each' : [id for id in user_ids if id != user_id]}}
                    },
                )
            )
        return bulk_operations
    
    
    @staticmethod
    def _get_bulk_operation_for_remove_planned_meeting(user_ids : list[UserID]) -> list[UpdateOne]:
        bulk_operations : list[UpdateOne] = []
        for user_id in user_ids:
            bulk_operations.append(
                UpdateOne(
                    {'_id' : user_id},
                    {
                        '$pull' : {'planned_user_ids' : {'$in' : [id for id in user_ids if id != user_id]}}
                    }
                )
            )
        return bulk_operations
    
    
    @staticmethod
    def _get_bulk_operation_for_add_complete_meeting(user_ids : list[UserID]) -> list[UpdateOne]:
        bulk_operations : list[UpdateOne] = []
        for user_id in user_ids:
            bulk_operations.append(
                UpdateOne(
                    {'_id' : user_id},
                    {
                        '$addToSet' : {'completed_user_ids' : {'$each' : [id for id in user_ids if id != user_id]}}
                    }
                )
            )
        return bulk_operations
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def add_new_planned_meeting(
                                        cls,
                                        collection : AsyncCollection, 
                                        user_ids : list[UserID]
                                    ) -> None:
        await collection.bulk_write(cls._get_bulk_operation_for_add_new_planned_meeting(user_ids))
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def cancel_meeting_for_users(
                                        cls,
                                        collection : AsyncCollection, 
                                        user_ids : list[UserID]
                                    ) -> None:
        await collection.bulk_write(cls._get_bulk_operation_for_remove_planned_meeting(user_ids))
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def complete_meeting_for_users(
                                        cls,
                                        collection : AsyncCollection, 
                                        user_ids : list[UserID]
                                    ) -> None:
        bulk_operations = [
                            *cls._get_bulk_operation_for_remove_planned_meeting(user_ids),
                            *cls._get_bulk_operation_for_add_complete_meeting(user_ids)
                        ]
        await collection.bulk_write(bulk_operations)
        
    
    
    
        
    
    


class UsersMeetingConcatinateDAO(MongoDAO):
    
    
    __slots__ = ('users_dao', 'meeting_dao', 'search_profile_dao')
    
    def __init__(
                    self, 
                    users_dao : UpdateUsersDAO, 
                    meeting_dao : MeetingsDAO,
                    search_profile_dao : SearchProfileDAO
                ) -> None:
        self.users_dao = users_dao
        self.meeting_dao = meeting_dao
        self.search_profile_dao = search_profile_dao
    
    
    
    async def create_new_meeting(
                                self, 
                                meeting_id : MeetingID, 
                                user_ids : list[UserID]
                            ) -> bool:
        all_users_exist = await self.users_dao.check_all_users_exist(user_ids)
        if not all_users_exist:
            return False
        
        await self.users_dao.add_new_planned_meeting(user_ids)
        await self.search_profile_dao.delete_users_profile(user_ids)
        await self.meeting_dao.create_new_meeting(meeting_id, user_ids)
        return True
        
        
    
    async def cancel_meeting(
                                self, 
                                meeting_id : MeetingID
                            ) -> bool:
        
        user_ids = await self.meeting_dao.delete_meeting(meeting_id)
        if user_ids is None:
            return False
        await self.users_dao.cancel_meeting_for_users(user_ids)
        return True
    
    
    
    async def complete_meeting(
                                self, 
                                meeting_id : MeetingID
                            ) -> bool:
        
        user_ids = await self.meeting_dao.delete_meeting(meeting_id)
        if user_ids is None:
            return False
        
        await self.users_dao.complete_meeting_for_users(user_ids)
        return True
    