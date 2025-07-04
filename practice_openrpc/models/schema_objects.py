from pydantic import BaseModel
from typing import Optional

class SchemaObject(BaseModel):
    title: str
    type: str
    description: str
    pattern: Optional[str] = None
