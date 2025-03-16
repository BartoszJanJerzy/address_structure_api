from uuid import uuid4
from fastapi import FastAPI
from logging import INFO, basicConfig
from src.common import *
from src.backend import celery_app, EndpointResult
from src.common.redis_connector import RedisConnector


basicConfig(level=INFO)
app = FastAPI(
    title="Awesome address structure app"
)
URL_STRUCT = "/struct"
URL_RESULT = "/result/{uuid}"


@app.post(URL_STRUCT, response_model=StructResponse)
async def endpoint_struct(order: StructRequest):
    record_id = str(uuid4())
    task = celery_app.send_task("src.backend.celery.structure_address", args=[order.model_dump(), record_id])
    return StructResponse(
        adr=order.adr,
        uuid=record_id
    )


@app.get(URL_RESULT, response_model=ResultResponse)
def endpoint_struct(uuid: str):
    result = EndpointResult().run(uuid)
    return ResultResponse(
        uuid=uuid,
        adr=result.data.adr,
        status=result.status,
        imie_nazwisko=result.data.name,
        ulica=result.data.street,
        numer_domu=result.data.house,
        kod_pocztowy=result.data.postal_code,
        miasto=result.data.city,
        wojewodztwo=result.data.voivodeship,
    )

