from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, Channel, ExchangeType
from faststream.rabbit.subscriber.asyncapi import AsyncAPISubscriber
from core.models.rabbitmq import rabbitmq_router, topic_exchange



CHANGE_TAGS_ROUTING_KEY = 'CHANGE_TAGS'

tags_publisher = rabbitmq_router.publisher(exchange = topic_exchange, routing_key = CHANGE_TAGS_ROUTING_KEY)

def get_tags_subscriber(queue : str, prefetch_count : int = 100) -> AsyncAPISubscriber:
    channel = Channel(prefetch_count)
    tags_queue = RabbitQueue(queue, arguments = {'x-max-priority' : 5}, routing_key = CHANGE_TAGS_ROUTING_KEY)
    return rabbitmq_router.subscriber(tags_queue, topic_exchange, channel = channel, retry = True)