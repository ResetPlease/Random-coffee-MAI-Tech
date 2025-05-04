from core.dao.mongo import MongoDAO, AsyncCollection
from core.param_decorator import class_parameter
from core.schemas import UserID
from app.base.schemas import SearchUserOut, ActiveSearchUserOut
from datetime import datetime



class UsersDAO(MongoDAO):
    
    
    
    @class_parameter()
    @MongoDAO.get_collection('users')
    async def get_user_by_id(cls, collection : AsyncCollection, user_id : UserID) -> SearchUserOut | None:
        user = await collection.find_one({'_id' : user_id})
        return SearchUserOut.model_validate(user) if user is not None else None
    
        

    @class_parameter()
    @MongoDAO.get_collection('users')
    async def get_searched_user_by_id(cls, collection : AsyncCollection, user_id : UserID) -> ActiveSearchUserOut | None:
        user = await collection.find_one(
                                            {
                                                '_id' : user_id,
                                                'is_search' : True 
                                            }
                                        )
        if user is None:
            return
        
        passed_meetings_count = 0
        
        for interval in user['meeting_intervals']:
            if interval['start'] > datetime.now():
                break
            passed_meetings_count += 1
            
        user['meeting_intervals'] = user['meeting_intervals'][passed_meetings_count:]
        
        return ActiveSearchUserOut.model_validate(user) if user is not None else None
        
        