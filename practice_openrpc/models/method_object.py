from pydantic import BaseModel
from typing import List
from .content_descriptor import ContentDescriptorObject
from .example_objects import ExamplePairingObject

class MethodObject(BaseModel):
    name: str
    summary: str
    description: str
    params: List[ContentDescriptorObject]
    result: ContentDescriptorObject
    examples: List[ExamplePairingObject]
