from pydantic import PositiveInt, EmailStr
from app.config import SMTPSettings
import random
from uuid import UUID, uuid4
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from core.models.rabbitmq.email import SendSimpleMessageForm
from core.models.rabbitmq.auth import AuthNotifyForm
from core.utils import BaseNotifyUtils




class EmailVerifyUtils(BaseNotifyUtils):
    
    __slots__ = ('code_length', 'smtp_settings', 'request_page_server', 'request_page_port', 'request_page_endpoint')
    
    def __init__(
                    self, 
                    publisher : AsyncAPIPublisher,
                    code_length : PositiveInt,
                    smtp_settings : SMTPSettings,
                    request_page_server : str,
                    request_page_port : int,
                    request_page_endpoint : str
                ) -> None:
        self.publisher = publisher
        self.code_length = code_length
        self.smtp_settings = smtp_settings
        self.request_page_server = request_page_server
        self.request_page_port = request_page_port
        self.request_page_endpoint = request_page_endpoint
        
        
    
    def generate_code(self) -> PositiveInt:
        min_value = 10 ** (self.code_length - 1)
        max_value = (10 ** self.code_length) - 1

        return random.randint(min_value, max_value)
    
    
    def generate_operation_id(self) -> UUID:
        return uuid4()
    
    
    
    async def send_email_with_code(self, code : PositiveInt, email : EmailStr) -> None:
        await self.publisher.publish(
                            SendSimpleMessageForm(
                                smtp_server = self.smtp_settings.SERVER,
                                smtp_port = self.smtp_settings.PORT,
                                receiver_email = email,
                                login = self.smtp_settings.LOGIN,
                                password = self.smtp_settings.PASSWORD,
                                subject = f'{code} is your verification code',
                                request_page_server = self.request_page_server,
                                request_page_endpoint = self.request_page_endpoint,
                                request_page_port = self.request_page_port,
                                request_page_query = {'code' : code}
                            )
                       )
        
        

class AuthVerifyUtils(BaseNotifyUtils):
        
        
    async def notify_about_user(self, op_id : UUID, email : EmailStr) -> None:
        await self.publisher.publish(AuthNotifyForm(operation_id = op_id, email = email))