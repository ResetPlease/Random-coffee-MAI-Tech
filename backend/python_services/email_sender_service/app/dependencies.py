from .utils import EmailSender
from functools import lru_cache








@lru_cache
def get_email_sender() -> EmailSender:
    return EmailSender()





