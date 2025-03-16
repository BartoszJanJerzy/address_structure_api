import yaml
from langchain_core.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_openai import ChatOpenAI
from logging import getLogger
from src.common import *


logger = getLogger("EndpointStruct")


class EndpointStruct:

    def __init__(self):
        self._redis_connector = RedisConnector()
        self._prompts = yaml.safe_load(open("resources/prompts.yaml", 'r'))
        self._config = yaml.safe_load(open("resources/config.yaml", 'r'))

    def run(self, order: StructRequest, record_id: str):
        self._save_pending(record_id)
        data = self._structure_text(order)
        self._save_done_record(data, record_id)

    def _structure_text(self, order: StructRequest) -> AddressSchema:
        logger.info("LLM job")
        model = ChatOpenAI(model=self._config["openai_model"])
        parser = PydanticOutputParser(pydantic_object=AddressSchema)
        prompt = PromptTemplate(
            template=self._prompts["json_parser_template"],
            input_variables=["text"],
            partial_variables={"format_instructions": parser.get_format_instructions()},
        )
        chain = prompt | model | parser
        data = chain.invoke({"text": order.adr})
        assert isinstance(data, AddressSchema), data
        return data

    def _save_done_record(self, data: AddressSchema, record_id: str):
        logger.info("Saving results")
        self._redis_connector.save_record(
            record_id=record_id,
            data=RedisRecord(
                status=EnumStatus.done,
                data=data
            ).model_dump()
        )

    def _save_pending(self, record_id: str):
        logger.info("logging PENDING")
        self._redis_connector.save_record(
            record_id=record_id,
            data=RedisRecord(status=EnumStatus.pending).model_dump()
        )
