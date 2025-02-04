from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .auth import auth_router


app = FastAPI(  
        root_path = '/api/auth',
        exception_handlers = {
        BaseHTTPException : http_exception_handler
    }
)

app.include_router(auth_router)