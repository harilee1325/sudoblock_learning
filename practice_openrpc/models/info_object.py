from pydantic import BaseModel, ConfigDict

class InfoObject(BaseModel):
    title: str
    version: str
    model_config = ConfigDict(extra="forbid")
