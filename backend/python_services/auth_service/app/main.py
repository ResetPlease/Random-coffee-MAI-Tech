from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .auth import auth_router
from .jwttoken import jwttoken_router
from .user_verify import user_verify_router
from core.dependencies.CORS import set_default_cors_policy


app = FastAPI(  
        root_path = '/api/auth',
        exception_handlers = {
        BaseHTTPException : http_exception_handler
    }
)

set_default_cors_policy(app)


app.include_router(auth_router)
app.include_router(jwttoken_router)
app.include_router(user_verify_router)