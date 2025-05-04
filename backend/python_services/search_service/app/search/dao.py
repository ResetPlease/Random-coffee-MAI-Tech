from core.dao.mongo import MongoDAO, AsyncCollection
from core.param_decorator import class_parameter, self_parameter
from core.schemas import UserID, TagID
from app.base import SearchUserOut
from typing import Any
from pydantic import PositiveInt, NonNegativeInt
from datetime import datetime
import logging

        
        




class UsersSearchDAO(MongoDAO):
    
    
    @staticmethod
    def get_main_search_condition(banned_user_ids : list[UserID], user_id : UserID) -> list[dict[str, Any]]:
        return  [
                    {
                        '$match' : {
                            'is_search' : True,
                            '_id' : {'$nin' : banned_user_ids},
                            'banned_user_ids' : {'$nin' : [user_id]}
                        }
                    }
                ]
        
        
        
    @staticmethod
    def get_tags_match_condition(tag_ids : list[TagID], min_tags_match : PositiveInt) -> list[dict[str, Any]]:
        return [
                    {
                        '$addFields' : {
                            'matched_tag_ids' : {
                                '$setIntersection' : ['$tag_ids', tag_ids]
                            }
                        }
                    },
                    {
                        '$addFields' : {
                            'matched_tags_count' : {'$size' : '$matched_tag_ids'}
                        }
                    },
                    {
                        '$match' : {
                            '$expr' : {
                                        '$gte' : [
                                            '$matched_tags_count',
                                            {'$max' : ['$min_tags_match', min_tags_match]}
                                        ]
                                    }
                        }
                    }
                ]
    
    @staticmethod
    def get_condition_for_datetime(
                                    date_start : datetime | None, 
                                    date_end : datetime | None,
                                    time_start : NonNegativeInt | None,
                                    time_end : NonNegativeInt | None
                                ) -> list[dict[str, Any]]:
        condition = [
                        {
                            '$addFields':  {
                                'meeting_intervals' : {
                                    '$filter' : {
                                        'input' : '$meeting_intervals',
                                        'as' : 'interval_now',
                                        'cond' : {
                                            '$gt' : ['$$interval_now.end', datetime.now()]
                                        }
                                    }
                                }
                            }
                        }
                    ]
        if date_start is not None and date_end is not None:
            condition.append(
                        {
                            '$addFields':  {
                                'meeting_intervals' : {
                                    '$filter' : {
                                        'input' : '$meeting_intervals',
                                        'as' : 'interval_now',
                                        'cond' : {
                                            '$and' : [
                                                {'$lte' : ['$$interval_now.start', date_end]},
                                                {'$gte' : ['$$interval_now.end', date_start]}
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    )
        if time_start is not None and time_end is not None:
            if time_start <= time_end:
                condition.append(
                        {
                            '$addFields':  {
                                'meeting_intervals' : {
                                    '$filter' : {
                                        'input' : '$meeting_intervals',
                                        'as' : 'interval_now',
                                        'cond' : {
                                            '$or' : [
                                                {
                                                    '$and' : [
                                                            {'$gte' : [{'$hour' : '$$interval_now.start'}, time_start]},
                                                            {'$lte' : [{'$hour' : '$$interval_now.start'}, time_end]}
                                                        ]
                                                },
                                                {
                                                    '$and' : [
                                                            {'$gte' : [{'$hour' : '$$interval_now.end'}, time_start]},
                                                            {'$lte' : [{'$hour' : '$$interval_now.end'}, time_end]}
                                                    ]
                                                }
                                            ]
                                        }
                                    }
                                }
                            }
                        }
                    )
            else:
                time_start, time_end = time_end, time_start
                condition.append(
                        {
                            '$addFields':  {
                                'meeting_intervals' : {
                                    '$filter' : {
                                        'input' : '$meeting_intervals',
                                        'as' : 'interval_now',
                                        'cond' : {
                                            '$not' : 
                                                [
                                                    {
                                                        '$and' : [
                                                            {
                                                                '$and' : [
                                                                    {'$gt' : [{'$hour' : '$$interval_now.start'}, time_start]},
                                                                    {'$lt' : [{'$hour' : '$$interval_now.start'}, time_end]}
                                                                ]
                                                            },
                                                            {
                                                                '$and' : [
                                                                    {'$gt' : [{'$hour' : '$$interval_now.end'}, time_start]},
                                                                    {'$lt' : [{'$hour' : '$$interval_now.end'}, time_end]}
                                                                ]
                                                            }
                                                        ]
                                                    }
                                                ]
                                        }
                                    }
                                }
                            }
                        }
                    )
                
                
        condition.append(
                        {
                            '$match' : {
                                'meeting_intervals' : {'$ne' : []}
                            }
                        }
                    )
        return condition
        
        
    @staticmethod
    def get_meeting_condition(user_id : UserID, only_new_users : bool) -> list[dict[str, Any]]:
        
        condition =  [
                        {
                            '$addFields' :
                                {
                                'have_planned_meeting' : {
                                    '$in': [user_id, '$planned_user_ids']
                                },
                                'have_completed_meeting' : {
                                    '$in': [user_id, '$completed_user_ids']
                                }
                            }
                        }
                    ]
        
        if only_new_users:
            condition.append(
                                {
                                    '$match' : {
                                        'have_planned_meeting' : False,
                                        'have_completed_meeting' : False
                                    }
                                }
                        )
        return condition
            
    
    
    @staticmethod
    def get_controll_fined_documents_condition(skip : PositiveInt, limit : PositiveInt) -> list[dict[str, Any]]:
        return [
                    {
                        '$project' : {
                                        'banned_user_ids' : 0,
                                        'planned_user_ids' : 0,
                                        'is_search' : 0,
                                        'completed_user_ids' : 0,
                                        'tag_ids' : 0,
                                        'min_tags_match' : 0,
                                        'exp' : 0
                                    }
                    },
                    {
                        '$sort' : {
                            'matched_tags_count' : -1,
                            'meeting_intervals.start' : 1
                        }
                    },
                    {
                        '$skip' : skip
                    },
                    {   
                        '$limit' : limit
                    }
                ]
    
        
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def search_users_by_params(
                                        cls,
                                        collection : AsyncCollection,
                                        searcher_user : SearchUserOut,
                                        only_new_users : bool,
                                        min_tags_match : PositiveInt,
                                        date_start : datetime | None,
                                        date_end : datetime | None,
                                        time_start : NonNegativeInt | None,
                                        time_end : NonNegativeInt | None,
                                        skip : PositiveInt,
                                        limit : PositiveInt
                                    ) -> list[dict[str, Any]]:
        search_condition = cls.get_main_search_condition(searcher_user.banned_user_ids, searcher_user.user_id)
        tag_condition = cls.get_tags_match_condition(searcher_user.tag_ids, min_tags_match)
        date_time_condition = cls.get_condition_for_datetime(date_start, date_end, time_start, time_end)
        meeting_condition = cls.get_meeting_condition(searcher_user.user_id, only_new_users)
        controller_condition = cls.get_controll_fined_documents_condition(skip, limit)
        
        response = await collection.aggregate([*search_condition, *tag_condition, *date_time_condition, *meeting_condition, *controller_condition])
        return await response.to_list()