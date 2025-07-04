from pydantic import BaseModel
from typing import Any, List

class ExampleObject(BaseModel):
    name: str
    value: Any

class ExamplePairingObject(BaseModel):
    name: str
    params: List[ExampleObject]
    result: ExampleObject
