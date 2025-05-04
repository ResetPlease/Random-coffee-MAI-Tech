from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, Channel
from faststream.rabbit.subscriber.asyncapi import AsyncAPISubscriber
from core.models.rabbitmq import rabbitmq_router, topic_exchange


CREATE_USER_ROUTING_KEY = 'CREATE_USER'

create_user_publisher = rabbitmq_router.publisher(exchange = topic_exchange, routing_key = CREATE_USER_ROUTING_KEY)

def get_create_user_subscriber(queue : str, prefetch_count : int = 100) -> AsyncAPISubscriber:
    user_create_channel = Channel(prefetch_count)
    user_create_queue = RabbitQueue(queue, routing_key = CREATE_USER_ROUTING_KEY)
    return rabbitmq_router.subscriber(user_create_queue, topic_exchange, channel = user_create_channel, retry = True)