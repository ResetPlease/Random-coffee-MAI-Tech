import aiohttp
from typing import Any
from .enums import HTTPType, HTTPResponseType


class HTTPRequest:
    
    
    @classmethod
    async def __send_request(
                            cls,
                            method : str,
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
        url_port : str = ''
        url_endpoint : str = ''

        if port is not None:
            url_port = f':{port}'
            
        if endpoint is not None:
            url_endpoint = endpoint if endpoint.startswith('/') else f'/{endpoint}'
              
        async with aiohttp.ClientSession() as session:
            response = await session.request(
                                   method = method,
                                   url = f'{http_type}://{server}{url_port}{url_endpoint}',
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
                    http_type : str = 'http',
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.__send_request('GET', server, http_type, port, endpoint, headers, query, None, cookies, response_method)
    
    
    @classmethod
    async def post(
                    cls,
                    server : str,
                    http_type : str = 'http',
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.__send_request('POST', server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    
    
    @classmethod
    async def put(
                    cls,
                    server : str,
                    http_type : str = 'http',
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.__send_request('PUT', server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    
    
    @classmethod
    async def delete(
                    cls,
                    server : str,
                    http_type : str = 'http',
                    port : int | None = None,
                    endpoint : str | None = None,
                    headers : dict[str, Any] | None = None,
                    query : dict[str, Any] | None = None,
                    body : dict[str, Any] | None = None,
                    cookies : dict[str, Any] | None = None,
                    response_method : HTTPResponseType | None = None
            ) -> aiohttp.ClientResponse | dict | str | bytes:
        return await cls.__send_request('DELETE', server, http_type, port, endpoint, headers, query, body, cookies, response_method)
    