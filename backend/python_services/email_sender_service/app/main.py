from faststream import FastStream
from fastapi import Depends
from core.models.rabbitmq import rabbitmq_router
from .dependencies import EmailSender, get_email_sender
from core.models.rabbitmq.email import send_simple_email_subscriber, SendSimpleMessageForm



app = FastStream(rabbitmq_router.broker)



@send_simple_email_subscriber
async def send_simple_email(
                            form : SendSimpleMessageForm, 
                            sender : EmailSender = Depends(get_email_sender) 
                        ) -> None:
    await sender.send_simple_email(form)
