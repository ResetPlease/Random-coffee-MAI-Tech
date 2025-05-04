from core.models.mongo import AsyncMongoClient, client
from core.param_decorator import self_parameter, func_parameter, AsyncCreatingParameterGenerator
from pymongo.asynchronous.collection import AsyncCollection
from pymongo.asynchronous.client_session import AsyncClientSession


class MongoDAO:
    
    
    @func_parameter()
    async def get_client() -> AsyncCreatingParameterGenerator[AsyncMongoClient]:
        yield client
    
    
    @func_parameter()
    async def get_collection(name : str, db : str = 'admin') -> AsyncCreatingParameterGenerator[AsyncCollection]:
        yield client[db][name]
        