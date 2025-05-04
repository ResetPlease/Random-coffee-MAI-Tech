from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .email_verify import email_verify_router
from core.models.rabbitmq import rabbitmq_router
from core.dependencies.CORS import set_default_cors_policy

app = FastAPI(
    root_path = '/api/email',
        exception_handlers = {
            BaseHTTPException : http_exception_handler
    }
)

set_default_cors_policy(app)


app.include_router(email_verify_router)
app.include_router(rabbitmq_router)