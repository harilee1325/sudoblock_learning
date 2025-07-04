# practice_openrpc.py
from pydantic import BaseModel, Field, constr
from typing import List, Optional, Any, Dict
from practise_rpc import MethodObject, eth_blockNumber_method
from practise_rpc import SchemaObject, ReferenceObject, ExampleObject, ExamplePairingObject, ContentDescriptorObject
from practise_rpc import BlockNumberHex
import json


# --- Part 1 & 2: All your existing models are perfect. No changes needed here. ---
# (SchemaObject, ReferenceObject, ExampleObject, etc.)

# --- NEW: Define Pydantic models for the ROOT OpenRPC Document Structure ---
class InfoObject(BaseModel):
    title: str
    version: str

class OpenRPCObject(BaseModel):
    openrpc: str = "1.3.2" # The version of the spec
    info: InfoObject
    methods: List[MethodObject]
    # We will add components later, but for now, this is enough.


# --- Part 3: All your existing method definitions are perfect. ---
# (block_number_schema, eth_blockNumber_method)

# --- Part 4: Assemble the FULL OpenRPC Document ---
# Instead of just dumping the method, we create an instance of our root OpenRPCObject.

full_openrpc_document = OpenRPCObject(
    info=InfoObject(
        title="My Practice Ethereum API",
        version="1.0.0"
    ),
    # The 'methods' field MUST be a list. We put our single method object inside it.
    methods=[
        eth_blockNumber_method 
    ]
)

# --- Part 5: Generate the Final JSON for the COMPLETE Document ---

# We now dump the full document object.
final_schema_dict = full_openrpc_document.model_dump(by_alias=True, exclude_none=True)

# Pretty-print the final result
print(json.dumps(final_schema_dict, indent=2))
