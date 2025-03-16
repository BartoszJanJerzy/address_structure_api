from dataclasses import dataclass
from yaml import safe_load


@dataclass(frozen=True)
class Config:
    redis_host: str
    redis_port: int

    openai_model: str

    celery_app: str
    celery_broker: str
    celery_backend: str


config = Config(**safe_load(open("resources/config.yaml", "r")))
