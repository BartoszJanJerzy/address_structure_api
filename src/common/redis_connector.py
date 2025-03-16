import json
import yaml
from redis import Redis
from src.common.schema import *


class RedisConnector:

    def __init__(self):
        config = yaml.safe_load(open("resources/config.yaml", "r"))
        self._client = Redis(
            host=config["redis_host"],
            port=config["redis_port"],
            health_check_interval=1,
            retry_on_error=[ConnectionError]    # add more if it's needed
        )

    def save_record(self, record_id: str, data: RedisRecord):
        self._client.set(record_id, json.dumps(data))

    def get_record(self, record_id: str) -> RedisRecord:
        raw_record: str | None = self._client.get(record_id)
        if raw_record:
            result = RedisRecord(**json.loads(raw_record))
        else:
            result = RedisRecord(
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
            )
        return result
