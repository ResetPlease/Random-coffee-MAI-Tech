from typing import Any
from pydantic import BaseModel, ConfigDict, Field
from fastapi.responses import JSONResponse
from fastapi import Request


class BaseHTTPExceptionModel(BaseModel):
    message : str = Field(description = 'Details')
    
    model_config = ConfigDict(frozen = True, extra = 'allow')
    



class BaseHTTPException(Exception):
    
    _all_responses_schemas : dict[type, dict[int, dict[str, Any]]] = {}
    
    def __init__(self, 
                status_code : int,
                detail : BaseHTTPExceptionModel,
                headers : dict[str, str] | None = None,
                cookies : dict[str, str | dict[str, str]] | None = None,
                response_schema : dict[str, Any] | None = None
            ) -> None:
        if status_code > 499 or status_code < 400:
            raise ValueError('status_code have incorrect value')
        
        self.status_code = status_code
        self.headers = headers
        self.cookies = cookies if cookies is not None else {}
        self.detail = {
                        'detail' : detail.model_dump()
                    }
        self.__registrate_new_obj(status_code, detail, response_schema)
    
    
    
    @classmethod    
    def get_responses_schemas(cls) -> dict[str, Any]:
        return cls._all_responses_schemas.get(cls)
    
    
    def __str__(self) -> str:
        return f'{self.status_code} : {self.detail}'
    
    
    def __registrate_new_obj(self,
                            status_code : int,
                            detail : BaseHTTPExceptionModel,
                            response_schema : dict[str, Any] | None = None
                        ) -> None:
        if response_schema is None:
            response_schema = {}
            
        response_schema['model'] = type(detail)
        class_response_schema = self._all_responses_schemas.get(self.__class__, {})
        
        if class_response_schema.get(status_code) is None:
            class_response_schema[status_code] = {}
        
        class_response_schema[status_code].update(response_schema.copy())
            
            
    
    def __init_subclass__(cls) -> None:
        cls._all_responses_schemas[cls] = {}
        for base_cls in cls.__bases__:
            if cls._all_responses_schemas.get(base_cls) is not None:
                cls._all_responses_schemas[cls].update(cls._all_responses_schemas[base_cls].copy())
        




async def http_exception_handler(request: Request, exc: BaseHTTPException) -> JSONResponse:
    
    response = JSONResponse(status_code = exc.status_code, content = exc.detail, headers = exc.headers)
    
    for key, value in exc.cookies.items():
        if isinstance(value, str):
            response.set_cookie(key = key, value = value)
        else:
            response.set_cookie(key = key, **value)
        
    return response
            
            