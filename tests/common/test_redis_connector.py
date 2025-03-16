import pytest
import json
from unittest.mock import patch, Mock
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


@patch("src.common.redis_connector.Redis")
def test_save_record(redis_mock):
    redis_mock.return_value = RedisMock()
    rc = RedisConnector()

    record_id = "super id"
    data = dict(super_key="super_value")

    rc.save_record(record_id, data)
    data_to_test = json.loads(rc._client.data[record_id])

    assert data_to_test == data, f"Left: {data_to_test}\tRight: {data}"


class TestGetRecord:

    @patch("src.common.redis_connector.Redis")
    def test_real_record(self, redis_mock):
        redis_mock.return_value = RedisMock()
        rc = RedisConnector()

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

        rc.save_record(record_id, data)
        data_to_test = rc.get_record(record_id).model_dump()

        assert data_to_test == data, f"Left: {data_to_test}\tRight: {data}"

    @patch("src.common.redis_connector.Redis")
    def test_none_existing_record(self, redis_mock):
        redis_mock.return_value = RedisMock()
        rc = RedisConnector()

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

        data_to_test = rc.get_record(record_id).model_dump()

        assert data_to_test == data, f"Left: {data_to_test}\tRight: {data}"