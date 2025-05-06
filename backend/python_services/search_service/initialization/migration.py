from core.dao.mongo import MongoDAO
from pymongo.asynchronous.collection import AsyncCollection
from core.param_decorator import self_parameter
import json
from datetime import datetime


class Initialization:
    
    
    __slots__ = ('need_init', )
    
    
    def __init__(self, need_init : bool) -> None:
        self.need_init = need_init
        
      
    @self_parameter()
    @MongoDAO.get_collection('meetings')
    async def create_meeting_collection(self, collection : AsyncCollection) -> None:
        meetings = json.load(open('./initialization/csv_data/user_meetings.csv'))
        await collection.create_index([('user_ids', 1)])
        await collection.insert_many(meetings)
    


    
    @self_parameter()
    @MongoDAO.get_collection('users')
    async def create_user_collection(self, collection : AsyncCollection) -> None:
        init_users = json.load(open('./initialization/csv_data/search.csv'))
        for user in (init_users):
            if not user['is_search']:
                continue
            user['exp'] = datetime.strptime(user['exp'], '%Y-%m-%d %H:%M:%S')
            user['meeting_intervals'] = [
                                                        {
                                                            'start' : datetime.strptime(interval['start'], '%Y-%m-%d %H:%M:%S'),
                                                            'end' : datetime.strptime(interval['end'], '%Y-%m-%d %H:%M:%S')
                                                        } 
                                                    for interval in user['meeting_intervals']
                                                ]



        await collection.create_index([('tag_ids', 1)])
        await collection.create_index([('banned_user_ids', 1)])
        await collection.create_index([('is_search', 1)])
        await collection.create_index(
                                    [('meeting_intervals.start', 1)],
                                    partialFilterExpression = {'is_search': True}
                                )
        await collection.create_index(
                                    [('meeting_intervals.end', 1)],
                                    partialFilterExpression = {'is_search': True}
                                )
        
        await collection.create_index(
                                    [('meeting_intervals.exp', 1)],
                                    partialFilterExpression = {'is_search': True}
                                )
        
        await collection.insert_many(init_users)



    async def run(self) -> None:
        if not self.need_init:
            return
        await self.create_user_collection()
        await self.create_meeting_collection()
        
        

