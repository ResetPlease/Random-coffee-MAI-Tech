from hashlib import sha256
from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher
from core.models.rabbitmq.user import CreateUserNotify
from core.dependencies.JWTToken import IssueTokensIn
from core.utils import BaseNotifyUtils




class AuthenticationUtils:
    
    @staticmethod
    def hashing_password(password : str) -> str:
        return sha256(password.encode()).hexdigest()



    
class NewUserNotifyUtils(BaseNotifyUtils):
        
    async def notify(self, form : IssueTokensIn) -> None:
        await self.publisher.publish(CreateUserNotify.model_validate(form))
        



