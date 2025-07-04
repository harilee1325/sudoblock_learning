# practice_openrpc.py
from pydantic import BaseModel, Field, constr
from typing import List, Optional, Any, Dict

# --- Part 1: Define Reusable Schema Primitives ---
# These are our building blocks, representing the data types in the JSON-RPC response.

BlockNumberHex = constr(pattern=r'^0x[a-fA-F0-9]+$')

# --- Part 2: Create Pydantic Models for the OpenRPC Specification Objects ---
# We are modeling the spec itself!

class SchemaObject(BaseModel):
    # A simplified model for JSON Schema for this example
    title: str
    type: str
    description: str
    pattern: Optional[str] = None

class ReferenceObject(BaseModel):
    ref: str = Field(..., alias='$ref')
    
    class Config:
        populate_by_name = True

class ExampleObject(BaseModel):
    name: str
    value: Any

class ExamplePairingObject(BaseModel):
    name: str
    params: List[ExampleObject]
    result: ExampleObject

class ContentDescriptorObject(BaseModel):
    name: str
    description: str
    # The schema can be a direct definition or a reference
    schema_: SchemaObject | ReferenceObject = Field(..., alias='schema')
    
    class Config:
        populate_by_name = True

class MethodObject(BaseModel):
    name: str
    description: str

    summary: str
    params: List[ContentDescriptorObject] # A list, even if empty
    result: ContentDescriptorObject
    examples: List[ExamplePairingObject]


# --- Part 3: Define the eth_blockNumber Method Using Our Pydantic Models ---

# First, define the reusable schema for the result.
# This would go into your `components/schemas` section.
block_number_schema = SchemaObject(
    title="BlockNumber",
    type="string",
    description="The number of the most recent block, represented as a hexadecimal string.",
    pattern="^0x[a-fA-F0-9]+$"
)

# Now, define the full MethodObject for eth_blockNumber as an instance of our Pydantic class.
eth_blockNumber_method = MethodObject(
    name="eth_blockNumber",
    summary="Gets the current block number.",
    description="Returns the number of the most recent block.",
    
    # The `params` list is empty, as per the spec.
    params=[], 
    
    # Define the result using a ContentDescriptorObject that references our schema.
    result=ContentDescriptorObject(
        name="blockNumber",
        description="The number of the most recent block the client is on.",
        schema_=ReferenceObject(**{"$ref": "#/components/schemas/BlockNumber"})
    ),
    
    # Define the examples.
    examples=[
        ExamplePairingObject(
            name="ethBlockNumberExample",
            params=[],
            result=ExampleObject(
                name="exampleBlockNumber",
                value="0x4b7"
            )
        )
    ]
)


# --- Part 4: Generate the Final JSON Schema ---

# Use .model_dump() to convert the Pydantic object into a dictionary.
# - by_alias=True ensures '$ref' is used instead of 'ref'.
# - exclude_none=True cleans up the output by removing optional fields that are None.
final_schema_dict = eth_blockNumber_method.model_dump(by_alias=True, exclude_none=True)

# Pretty-print the final result
#import json
#print(json.dumps(final_schema_dict, indent=2))