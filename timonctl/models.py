from datetime import datetime
from typing import Dict
import uuid as uuid_pkg

from pydantic import BaseModel, Json


class Result(BaseModel):
    status_code: int
    headers: Dict
    message: str = ""
    data: Json


class TimonBaseModel(BaseModel):
    id: uuid_pkg.UUID
    created_at: datetime
    updated_at: datetime

    # https://python.tutorialink.com/short-way-to-get-all-field-names-of-a-pydantic-class/
    @classmethod
    def get_field_names(cls, alias=False):
        return list(cls.schema(alias).get("properties").keys())


class Blueprint(TimonBaseModel):
    name: str


class Environment(TimonBaseModel):
    name: str
