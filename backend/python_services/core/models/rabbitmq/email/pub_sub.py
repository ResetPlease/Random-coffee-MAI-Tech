from faststream.rabbit import RabbitExchange, RabbitQueue, Channel
from core.models.rabbitmq import rabbitmq_router, direct_exchenge



send_simple_email_queue = RabbitQueue('send-simple-email-queue')
send_simple_email_chennel = Channel(2)
send_simple_email_publisher = rabbitmq_router.publisher(send_simple_email_queue, direct_exchenge)
send_simple_email_subscriber = rabbitmq_router.subscriber(send_simple_email_queue, direct_exchenge, channel = send_simple_email_chennel)
