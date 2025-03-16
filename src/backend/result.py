from logging import getLogger
from src.common import *


logger = getLogger("EndpointResult")


class EndpointResult:

    def __init__(self):
        self._redis_connector = RedisConnector()

    def run(self, record_id: str) -> RedisRecord:
        logger.info("Getting result")
        result = self._redis_connector.get_record(record_id)
        return result