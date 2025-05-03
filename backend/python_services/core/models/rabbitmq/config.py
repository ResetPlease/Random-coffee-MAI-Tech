from pydantic_settings import SettingsConfigDict
from core.models.base import BaseSettings


class RabbitMQSettings(BaseSettings):
    USER : str
    VHOST : str
    
    model_config = SettingsConfigDict(
        env_prefix = 'RABBITMQ_',
        extra = 'ignore',
        frozen = True
    )

rabbitmq_settings = RabbitMQSettings()


def get_url() -> str:
    return (f'amqp://{rabbitmq_settings.USER}:{rabbitmq_settings.PASSWORD}'
            f'@{rabbitmq_settings.HOST}:{rabbitmq_settings.PORT}/{rabbitmq_settings.VHOST}')
    
