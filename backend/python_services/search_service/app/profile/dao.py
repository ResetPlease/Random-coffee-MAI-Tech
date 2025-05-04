from core.dao.mongo import MongoDAO, AsyncCollection
from core.param_decorator import class_parameter, self_parameter
from core.schemas import UserID, TagID, DateTimeIntervalIn
from app.base import IncorrectUserIDError
from pydantic import NonNegativeInt
from .errors import IncorrectMinMatchTagsError
from datetime import datetime











class SearchProfileDAO(MongoDAO):
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def delete_profile_with_expaired_meetings(cls, collection : AsyncCollection, exp : datetime) -> None:
        await collection.update_many(
                                    {
                                       'is_search' : True,
                                       'exp' : {'$lte' : exp}
                                    },
                                    {
                                        '$set' : {
                                            'is_search' : False
                                        },
                                        '$unset' : {
                                            'min_tags_match' : 1,
                                            'meeting_intervals' : 1,
                                            'exp' : 1
                                        }
                                    }
                                )
        
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def delete_users_profile(cls, collection : AsyncCollection, user_ids : list[UserID]) -> None:
        await collection.update_many(
                                    {
                                       '_id' : {'$in' : user_ids}
                                    },
                                    {
                                        '$set' : {
                                            'is_search' : False
                                        },
                                        '$unset' : {
                                            'min_tags_match' : 1,
                                            'meeting_intervals' : 1,
                                            'exp' : 1
                                        }
                                    }
                                )
    
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def delete_user_profile(
                                    cls,
                                    collection : AsyncCollection, 
                                    user_id : UserID
                                ) -> None:
        await collection.update_one(
                                    {'_id' : user_id},
                                    {
                                        '$set' : {
                                            'is_search' : False
                                        },
                                        '$unset' : {
                                            'min_tags_match' : 1,
                                            'meeting_intervals' : 1,
                                            'exp' : 1
                                        }
                                    }
                                )
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def create_or_update_user_profile(
                                    cls,
                                    collection : AsyncCollection, 
                                    user_id : UserID, 
                                    min_match_tags : NonNegativeInt,
                                    sorted_meeting_intervals : list[DateTimeIntervalIn]
                                ) -> None:
        user = await collection.find_one({'_id' : user_id})
        
        if user is None:
            raise IncorrectUserIDError
        
        if len(user['tag_ids']) < min_match_tags:
            raise IncorrectMinMatchTagsError
        
        await collection.update_one(
                                    {'_id' : user_id},
                                    {
                                        '$set' : {
                                            'is_search' : True,
                                            'min_tags_match' : min_match_tags,
                                            'meeting_intervals' : [
                                                                meeting_interval.model_dump() for meeting_interval in sorted_meeting_intervals
                                                            ],
                                            'exp' : sorted_meeting_intervals[-1].start
                                        }
                                    }
                                )
        