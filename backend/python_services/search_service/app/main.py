from fastapi import FastAPI
from core.exception import BaseHTTPException, http_exception_handler
from .profile.dependencies import run_clear_profile
from .search import search_router
from .update_users import update_users_router
from .profile import search_profile_router
from core.dependencies.CORS import set_default_cors_policy


app = FastAPI(  
        root_path = '/api',
        docs_url = '/search/docs',
        openapi_url = '/search/openapi.json',
        exception_handlers = {
            BaseHTTPException : http_exception_handler
    },
        on_startup = [run_clear_profile]
)



set_default_cors_policy(app)

app.include_router(search_router, prefix = '/search')
app.include_router(update_users_router, prefix = '/search')
app.include_router(search_profile_router, prefix = '/search')