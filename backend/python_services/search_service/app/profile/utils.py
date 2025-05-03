from .dao import SearchProfileDAO
from datetime import timedelta, datetime
import asyncio
import logging



class SearchProfileUtils:
    
    
    __slots__ = ('search_profile_dao', 'waiting_time')
    
    def __init__(self, search_profile_dao : SearchProfileDAO, waiting_time : timedelta) -> None:
        self.search_profile_dao = search_profile_dao
        self.waiting_time = waiting_time
    
    
    async def run_infinity_cleaning_cycle(self) -> None:
        while True:
            await self.search_profile_dao.delete_profile_with_expaired_meetings(datetime.now())
            await asyncio.sleep(self.waiting_time.total_seconds())
        