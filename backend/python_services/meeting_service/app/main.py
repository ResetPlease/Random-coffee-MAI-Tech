from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .ban import users_ban_router
from .meetings import meeting_router
from .notify import notify_router
from core.dependencies.CORS import set_default_cors_policy


app = FastAPI(  
        root_path = '/api/meetings',
        exception_handlers = {
            BaseHTTPException : http_exception_handler
    }
)

set_default_cors_policy(app)



app.include_router(users_ban_router)
app.include_router(meeting_router)
app.include_router(notify_router)