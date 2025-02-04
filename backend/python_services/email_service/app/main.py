from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .email_verify import email_verify_router



app = FastAPI(
    root_path = '/api/email',
        exception_handlers = {
            BaseHTTPException : http_exception_handler
    }
)

app.include_router(email_verify_router)