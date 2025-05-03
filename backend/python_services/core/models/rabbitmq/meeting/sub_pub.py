from faststream.rabbit import RabbitExchange, RabbitQueue, RabbitBroker, Channel, ExchangeType
from faststream.rabbit.subscriber.asyncapi import AsyncAPISubscriber
from core.models.rabbitmq import rabbitmq_router, topic_exchange



MEETING_ROUTING_KEY = 'MEETINGS'

meeting_publisher = rabbitmq_router.publisher(exchange = topic_exchange, routing_key = MEETING_ROUTING_KEY)

def get_meeting_subscriber(queue : str, prefetch_count : int = 100) -> AsyncAPISubscriber:
    channel = Channel(prefetch_count)
    meeting_queue = RabbitQueue(queue, arguments = {'x-max-priority' : 5}, routing_key = MEETING_ROUTING_KEY)
    return rabbitmq_router.subscriber(meeting_queue, topic_exchange, channel = channel, retry = True)