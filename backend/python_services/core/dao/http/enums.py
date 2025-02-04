from enum import StrEnum, auto


class HTTPType(StrEnum):
    HTTP = auto()
    HTTPS = auto()
    
    
class HTTPResponseType(StrEnum):
    JSON = auto()
    TEXT = auto()
    BYTES = auto()
    