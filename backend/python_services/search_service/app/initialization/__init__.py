from .migration import Initialization



async def run_initialization() -> None:
    from app.base.config import search_service_settings
    
    return await Initialization(search_service_settings.NEED_INIT).run()