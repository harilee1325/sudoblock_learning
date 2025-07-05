from typing import List, Dict, Any
from pydantic import BaseModel, ConfigDict
from .info_object import InfoObject
from .method_object import MethodObject

class OpenRPCObject(BaseModel):
    openrpc: str = "1.3.2"
    info: InfoObject
    methods: List[MethodObject]
    components: Dict[str, Any] | None = None

    model_config = ConfigDict(extra="forbid")
