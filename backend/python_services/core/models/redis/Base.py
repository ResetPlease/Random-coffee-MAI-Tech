from redis.asyncio import Redis
from .config import redis_settings


client = Redis(
                host = redis_settings.HOST,
                port = redis_settings.PORT,
                password = redis_settings.PASSWORD,
                db = redis_settings.DB
            )

