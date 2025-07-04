from pydantic import BaseModel

class InfoObject(BaseModel):
    title: str
    version: str
