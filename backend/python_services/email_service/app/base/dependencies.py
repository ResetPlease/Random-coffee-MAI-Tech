from functools import lru_cache
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher



@lru_cache
def get_send_simple_email_publisher() -> AsyncAPIPublisher:
    from core.models.rabbitmq.email import send_simple_email_publisher
    
    return send_simple_email_publisher


