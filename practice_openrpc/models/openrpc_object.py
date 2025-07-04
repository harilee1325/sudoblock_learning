from pydantic import BaseModel
from typing import List
from .info_object import InfoObject
from .method_object import MethodObject
from typing import Optional, Dict, Any

class OpenRPCObject(BaseModel):
    openrpc: str = "1.3.2"          # spec version
    info: InfoObject                # mandatory
    methods: List[MethodObject]     # at least []
    components: Optional[Dict[str, Any]] = None

    # You’ll add `components`, `servers`, etc. later as needed
