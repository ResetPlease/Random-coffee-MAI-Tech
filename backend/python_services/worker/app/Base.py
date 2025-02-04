from celery import Celery
from .config import get_backend_url, get_broker_url



celery = Celery('worker', broker = get_broker_url(), backend = get_backend_url())
celery.autodiscover_tasks(['worker.app.email'], force = True)