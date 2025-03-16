from pydantic import BaseModel, Field
from enum import Enum


class StructRequest(BaseModel):
    adr: str


class StructResponse(BaseModel):
    adr: str
    uuid: str


class AddressSchema(BaseModel):
    """A schema for structured address information"""
    adr: str = Field(description="Full raw address from the given text")
    name: str = Field(description="Name and Surname found in a given text")
    street: str = Field(description="The street found in a given text")
    house: str = Field(description="House number found in a given text")
    postal_code: str = Field(description="Postal code found in a given text")
    city: str = Field(description="City found in a given text")
    voivodeship: str = Field(description="Voivodeship found in a given text")


class EnumStatus(str, Enum):
    unknown: str = "UNKNOWN"
    pending: str = "PENDING"
    done: str = "DONE"


class RedisRecord(BaseModel):
    status: EnumStatus
    data: AddressSchema | None = None


class ResultResponse(BaseModel):
    uuid: str
    adr: str
    status: EnumStatus
    imie_nazwisko: str
    ulica: str
    numer_domu: str
    kod_pocztowy: str
    miasto: str
    wojewodztwo: str