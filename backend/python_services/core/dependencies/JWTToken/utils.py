
from core.dao.http import HTTPRequest, HTTPMethod
from .schemas import IssuedJWTTokenPayloadOut, AuthAPIHeaderIn
from core.utils import BaseServiceUtils
from typing import Any
from fastapi import HTTPException, status
from .errors import JWTException, JWTExceptionModel, IsNotSpecifiedError






class AuthServiceUtils(BaseServiceUtils):
    
    
    __slots__ = ('verify_endpoint', 'verify_endpoint_method')
    
    
    def __init__(
                self, 
                requester : HTTPRequest,
                service_name : str, 
                service_port : int,
                verify_endpoint : str,
                verify_endpoint_method : HTTPMethod
            ) -> None:
        self.verify_endpoint = verify_endpoint
        self.verify_endpoint_method = verify_endpoint_method
        super().__init__(requester, service_name, service_port)


    async def verify(self, auth_header : AuthAPIHeaderIn) -> IssuedJWTTokenPayloadOut:
        if auth_header is None:
            raise IsNotSpecifiedError
        
        response = await self.requester.request(   
                                                    method = self.verify_endpoint_method,
                                                    server = self.service_name,
                                                    port = self.service_port,
                                                    endpoint = self.verify_endpoint,
                                                    headers = {'Authorization' : auth_header}                       
                                                )
        
        response_json : dict[str, Any] = await response.json()

        if response_json.get('detail') is not None:
            if response.status == status.HTTP_422_UNPROCESSABLE_ENTITY:
                raise HTTPException(status_code = response.status, detail = response_json['detail'])
            
            raise JWTException(
                                response.status, 
                                JWTExceptionModel.model_validate(response_json['detail']),
                                response.headers,
                                response.cookies,
                                need_registrate = False
                            )
            
        return IssuedJWTTokenPayloadOut.model_validate(response_json)  



