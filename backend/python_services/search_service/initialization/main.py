import sys
from os.path import abspath, dirname

sys.path.append(dirname(dirname(abspath(__file__))))

from migration import Initialization
from app.base.config import search_service_settings
import asyncio







async def main() -> None:
    init = Initialization(search_service_settings.NEED_INIT)
    await init.run()
    
    
    
if __name__ == '__main__':
    asyncio.run(main())
    
