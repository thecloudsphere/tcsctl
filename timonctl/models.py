from datetime import datetime
from typing import Dict, Optional
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


# blueprint

class BlueprintBase(BaseModel):
    name: Optional[str]
    repository: Optional[str]
    repository_server: Optional[str]


class Blueprint(TimonBaseModel, BlueprintBase):
    pass


# environment

class EnvironmentBase(BaseModel):
    name: Optional[str]
    repository: Optional[str]
    repository_server: Optional[str]


class Environment(TimonBaseModel, EnvironmentBase):
    pass
