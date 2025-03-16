from celery import Celery
from src.common import *
from .struct import EndpointStruct


celery_app = Celery(
    config.celery_app,
    broker=config.celery_broker,
    backend=config.celery_backend
)


@celery_app.task
def structure_address(order: dict, record_id: str):
    EndpointStruct().run(StructRequest(**order), record_id)
