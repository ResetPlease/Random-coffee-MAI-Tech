from core.schemas import BaseModel
from typing import Any



class SendSimpleMessageForm(BaseModel):
    smtp_server : str
    smtp_port : int
    receiver_email : str
    subject : str
    login : str
    password : str
    request_page_server : str
    request_page_port : int
    request_page_endpoint : str
    request_page_query : dict[str, Any] | None = None
    request_page_headers : dict[str, Any] | None = None
    
    
    