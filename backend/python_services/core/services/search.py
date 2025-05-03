from pydantic_settings import BaseSettings, SettingsConfigDict
from core.dao.http import HTTPMethod





class SearchServiceSettings(BaseSettings):
    NAME : str
    PORT : int
    MATCH_ENDPOINT : str
    MATCH_ENDPOINT_METHOD : HTTPMethod
    
    model_config = SettingsConfigDict(
        env_prefix = 'SEARCH_SERVICE_',
        extra = 'ignore',
        frozen = True
    )
    
search_service_settings = SearchServiceSettings()
