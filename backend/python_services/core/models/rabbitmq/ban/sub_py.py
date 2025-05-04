from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, Channel, ExchangeType
from faststream.rabbit.subscriber.asyncapi import AsyncAPISubscriber
from core.models.rabbitmq import rabbitmq_router, topic_exchange



BAN_ROUTING_KEY = 'USERS_BAN'

ban_publisher = rabbitmq_router.publisher(exchange = topic_exchange, routing_key = BAN_ROUTING_KEY)

def get_ban_subscriber(queue : str, prefetch_count : int = 100) -> AsyncAPISubscriber:
    channel = Channel(prefetch_count)
    ban_queue = RabbitQueue(queue, arguments = {'x-max-priority' : 5}, routing_key = BAN_ROUTING_KEY)
    return rabbitmq_router.subscriber(ban_queue, topic_exchange, channel = channel, retry = True)