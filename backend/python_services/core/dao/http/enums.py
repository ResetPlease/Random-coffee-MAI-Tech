from enum import StrEnum, auto


class HTTPType(StrEnum):
    HTTP = auto()
    HTTPS = auto()
    
    
class HTTPMethod(StrEnum):
    GET = auto()
    POST = auto()
    PUT = auto()
    DELETE = auto()
    
    
class HTTPResponseType(StrEnum):
    JSON = auto()
    TEXT = auto()
    BYTES = auto()
    