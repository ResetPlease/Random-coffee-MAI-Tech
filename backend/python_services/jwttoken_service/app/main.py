from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .jwttoken import jwttoken_router

app = FastAPI(  
        root_path = '/api/jwttoken',
        exception_handlers = {
        BaseHTTPException : http_exception_handler
    }
)

app.include_router(jwttoken_router)