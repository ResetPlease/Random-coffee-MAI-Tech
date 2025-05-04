from core.dao.http import HTTPRequest






class BaseServiceUtils:
    
    __slots__ = ('requester', 'service_name', 'service_port')
    
    def __init__(
                self, 
                requester : HTTPRequest,
                service_name : str, 
                service_port : int
            ) -> None:
        self.requester = requester
        self.service_name = service_name
        self.service_port = service_port
        