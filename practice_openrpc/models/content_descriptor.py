from pydantic import BaseModel, Field
from typing import Union
from .schema_objects import SchemaObject

class ReferenceObject(BaseModel):
    ref: str = Field(..., alias='$ref')

    class Config:
        populate_by_name = True

class ContentDescriptorObject(BaseModel):
    name: str
    description: str
    # Either inline schema or $ref
    schema_: Union[SchemaObject, ReferenceObject] = Field(..., alias='schema')

    class Config:
        populate_by_name = True
