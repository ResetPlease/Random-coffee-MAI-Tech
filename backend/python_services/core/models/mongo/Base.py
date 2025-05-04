from pymongo import AsyncMongoClient
from .config import get_url

client = AsyncMongoClient(get_url())