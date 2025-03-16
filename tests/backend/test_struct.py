import pytest
import json
from unittest.mock import patch, Mock
from src.backend import EndpointStruct
from src.common import RedisConnector, RedisRecord, EnumStatus, AddressSchema, StructRequest


class RedisMock:

    def __init__(self, *args, **kwargs):
        self.data = {}

    def set(self, record_id, data):
        self.data[record_id] = data

    def get(self, record_id):
        if record_id in self.data.keys():
            return self.data[record_id]
        else:
            return None


@patch("src.common.redis_connector.Redis")
def test_save_pending(redis_mock):
    redis_mock.return_value = RedisMock()
    record_id = "super id"
    endpoint = EndpointStruct()
    endpoint._save_pending(record_id)

    data_to_test = json.loads(endpoint._redis_connector._client.data[record_id])
    data = RedisRecord(
        status=EnumStatus.pending,
        data=None
    ).model_dump()
    assert data_to_test == data


@patch("src.common.redis_connector.Redis")
def test_save_done(redis_mock):
    redis_mock.return_value = RedisMock()

    record_id = "super id"
    data = AddressSchema(
        adr="adr",
        name="name",
        street="street",
        house="house",
        postal_code="postal_code",
        city="city",
        voivodeship="voiv",
    )

    endpoint = EndpointStruct()
    endpoint._save_done_record(data, record_id)

    data_to_test = json.loads(endpoint._redis_connector._client.data[record_id])
    record_expected = RedisRecord(
        status=EnumStatus.done,
        data=data
    ).model_dump()
    assert data_to_test == record_expected


@patch("src.common.redis_connector.Redis")
@patch.object(EndpointStruct, "_structure_text")
def test_run(structure_text_mock: Mock, redis_mock: Mock):
    address_data = AddressSchema(
        adr="Tadeusz Pudełko al.Pieczywskie 21, Poznań, wielkopolskie, 56-890",
        name="Tadeusz Pudełko",
        street="al.Pieczywskie",
        house="21",
        postal_code="56-890",
        city="Poznań",
        voivodeship="wielkopolskie",
    )
    record_id = "super id"

    redis_mock.return_value = RedisMock()
    structure_text_mock.return_value = address_data

    es = EndpointStruct()
    es.run(
        StructRequest(adr="Tadeusz Pudełko al.Pieczywskie 21, Poznań, wielkopolskie, 56-890"),
        record_id
    )

    structure_text_mock.assert_called_once()
    saved_record = json.loads(es._redis_connector._client.data[record_id])
    expected_record = RedisRecord(
        status=EnumStatus.done,
        data=address_data
    ).model_dump()
    assert saved_record == expected_record

