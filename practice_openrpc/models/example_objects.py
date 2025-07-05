from typing import Any, List
from pydantic import BaseModel, ConfigDict

class ExampleObject(BaseModel):
    name: str
    value: Any
    model_config = ConfigDict(extra="forbid")

class ExamplePairingObject(BaseModel):
    name: str
    params: List[ExampleObject]
    result: ExampleObject
    model_config = ConfigDict(extra="forbid")
