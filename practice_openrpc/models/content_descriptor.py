from typing import Union
from pydantic import BaseModel, Field, ConfigDict
from .schema_objects import SchemaObject

class ReferenceObject(BaseModel):
    ref: str = Field(..., alias="$ref")
    model_config = ConfigDict(populate_by_name=True, extra="forbid")

class ContentDescriptorObject(BaseModel):
    name: str
    description: str
    schema_: Union[SchemaObject, ReferenceObject] = Field(..., alias="schema")
    model_config = ConfigDict(populate_by_name=True, extra="forbid")
