from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .user_tags import user_tags_router
from .tags import tags_router
from .notify import notify_router
from core.dependencies.CORS import set_default_cors_policy


app = FastAPI(
    root_path="/api",
    docs_url="/tags/docs",
    openapi_url="/tags/openapi.json",
    exception_handlers={BaseHTTPException: http_exception_handler},
)

set_default_cors_policy(app)

app.include_router(user_tags_router, prefix="/tags")
app.include_router(tags_router, prefix="/tags")
app.include_router(notify_router, prefix="/tags")
