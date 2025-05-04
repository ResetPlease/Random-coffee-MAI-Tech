from .dao import SearchProfileDAO
from functools import lru_cache
from .utils import SearchProfileUtils
from fastapi import Depends
import asyncio


@lru_cache
def get_search_profile_dao() -> SearchProfileDAO:
    return SearchProfileDAO()


@lru_cache
def get_search_profile_utils() -> SearchProfileUtils:
    from app.base.config import search_service_settings
    
    return SearchProfileUtils(SearchProfileDAO(), search_service_settings.MEETING_CLEAR_TIMEDELATA)



async def run_clear_profile() -> None:
    utils = get_search_profile_utils()
    asyncio.create_task(utils.run_infinity_cleaning_cycle())