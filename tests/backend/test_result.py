import pytest
import json
from unittest.mock import patch, Mock
from src.backend import EndpointResult
from src.common import RedisConnector, RedisRecord, EnumStatus, AddressSchema


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


class TestEndpoint:

    @patch("src.common.redis_connector.Redis")
    def test_real_record(self, redis_mock):
        redis_mock.return_value = RedisMock()

        record_id = "super id"
        data = RedisRecord(
            status=EnumStatus.done,
            data=AddressSchema(
                adr="adr",
                name="name",
                street="street",
                house="house",
                postal_code="postal_code",
                city="city",
                voivodeship="voiv",
            )
        ).model_dump()

        endpoint = EndpointResult()
        endpoint._redis_connector._client.data = {record_id: json.dumps(data)}
        data_to_test = endpoint.run(record_id).model_dump()

        assert data_to_test == data, f"Left: {data_to_test}\tRight: {data}"

    @patch("src.common.redis_connector.Redis")
    def test_none_existing_record(self, redis_mock):
        redis_mock.return_value = RedisMock()

        record_id = "super id"
        data = RedisRecord(
            status=EnumStatus.unknown,
            data=AddressSchema(
                adr="",
                name="",
                street="",
                house="",
                postal_code="",
                city="",
                voivodeship="",
            )
        ).model_dump()

        endpoint = EndpointResult()
        data_to_test = endpoint.run(record_id).model_dump()

        assert data_to_test == data, f"Left: {data_to_test}\tRight: {data}"