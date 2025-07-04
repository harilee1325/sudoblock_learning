from pydantic import BaseModel, constr
from pprint import pprint

# Define a Pydantic model for the result
class BlockNumberResult(BaseModel):
    block_number: constr(pattern=r'^0x[a-fA-F0-9]+$')

# Generate the schema for just this piece
# This isn't the whole MethodObject, just the 'schema' part of the result.
schema_for_result = BlockNumberResult.model_json_schema()['properties']['block_number']
# Add a title and description for clarity
schema_for_result['title'] = "BlockNumber"
schema_for_result['description'] = "The number of the most recent block, represented as a hexadecimal string."

pprint(schema_for_result)