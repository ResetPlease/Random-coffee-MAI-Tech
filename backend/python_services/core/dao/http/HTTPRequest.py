import aiohttp
from typing import Any
from .enums import HTTPType, HTTPResponseType, HTTPMethod


class HTTPRequest:
    
    
    @staticmethod
    def get_url(    
                server : str,
                http_type : HTTPType = HTTPType.HTTP,
                port : int | None = None,
                endpoint : str | None = None
            ) -> str:
        url_port : str = ''
        url_endpoint : str = ''

        if port is not None:
            url_port = f':{port}'
            
        if endpoint is not None:
            url_endpoint = endpoint.removeprefix('/') if endpoint.startswith('/') else endpoint
        
        return f'{http_type}://{server}{url_port}/{url_endpoint}'

        
        
    
    
    
    @classmethod
    async def request(
                            cls,
                            method : HTTPMethod,
                            server : str,
                            http_type : HTTPType = HTTPType.HTTP,
                            port : int | None = None,
                            endpoint : str | None = None,
                            headers : dict[str, Any] | None = None,
                            query : dict[str, Any] | None = None,
                            body : dict[str, Any] | None = None,
                            cookies : dict[str, Any] | None = None,
                            response_method : HTTPResponseType | None = None
                        ) -> aiohttp.ClientResponse | dict[str, Any] | str | bytes:
              
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                                               method = method.name,
                                               url = cls.get_url(server, http_type, port, endpoint),
                                               params = query,
                                               headers = headers,
                                               allow_redirects = False,
                                               cookies = cookies,
                                               json = body
                                            )
            match response_method:
                case HTTPResponseType.JSON:
                    return await response.json()
                case HTTPResponseType.TEXT:
                    return await response.text()
                case HTTPResponseType.BYTES:
                    return await response.read()
                case _:
                    return response
                    
                    
                    
                

    
    @classmethod
    async def get(
                    cls,
                    server : str,
                    http_type : HTTPType = HTTPType.HTTP,
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.request(HTTPMethod.GET, server, http_type, port, endpoint, headers, query, None, cookies, response_method)
    
    
    @classmethod
    async def post(
                    cls,
                    server : str,
                    http_type : HTTPType = HTTPType.HTTP,
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.request(HTTPMethod.POST, server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    
    
    @classmethod
    async def put(
                    cls,
                    server : str,
                    http_type : HTTPType = HTTPType.HTTP,
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.request(HTTPMethod.PUT, server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    
    
    @classmethod
    async def delete(
                    cls,
                    server : str,
                    http_type : HTTPType = HTTPType.HTTP,
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.request(HTTPMethod.DELETE, server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    