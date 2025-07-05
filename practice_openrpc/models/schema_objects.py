from pydantic import BaseModel, ConfigDict, Field

class SchemaObject(BaseModel):
    title: str
    type: str
    description: str
    pattern: str | None = None

    # Pydantic-v2 style — no inner class
    model_config = ConfigDict(extra="forbid")
