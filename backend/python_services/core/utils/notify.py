from faststream.rabbit.publisher.asyncapi import AsyncAPIPublisher






class BaseNotifyUtils:
    
    
    __slots__ = ('publisher', )
    
    
    def __init__(
                    self,
                    publisher : AsyncAPIPublisher
            ) -> None:
        self.publisher = publisher
        