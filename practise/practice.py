# practice.py
from pydantic import BaseModel, Field, ValidationError
from pprint import pprint
import jsonschema

def inspect_model(model: type[BaseModel], data: dict):
    """A helper function to validate data and print schema."""
    print("="*50)
    print(f"MODEL: {model.__name__}")
    print("-" * 20)
    
    # 1. Validate with Pydantic
    print("--- Pydantic Validation ---")
    try:
        instance = model(**data)
        print("Pydantic validation SUCCESSFUL!")
        pprint(instance.model_dump())
    except ValidationError as e:
        print("Pydantic validation FAILED:")
        print(e)
    
    # 2. Generate and print the JSON Schema
    print("\n--- Generated JSON Schema ---")
    schema = model.model_json_schema()
    pprint(schema)

    # 3. Validate with the jsonschema library
    print("\n--- jsonschema Library Validation ---")
    try:
        jsonschema.validate(instance=data, schema=schema)
        print("jsonschema validation SUCCESSFUL!")
    except jsonschema.exceptions.ValidationError as e:
        print(f"jsonschema validation FAILED: {e.message}")
    print("="*50)


# --- Level 1: Solution ---
from pydantic import EmailStr
from typing import Optional

class UserProfile(BaseModel):
    username: str
    email: EmailStr  # Pydantic has built-in types for common formats!
    age: Optional[int] = None # Use Optional for fields that can be None
    is_active: bool = True

# --- Test Cases ---
valid_user_data = {
    "username": "alice",
    "email": "alice@example.com"
}
# Note: We omit age and is_active to test the defaults.

invalid_user_data = {
    "username": "bob",
    "email": "bob@invalid-email" # Invalid email format
}
# Note: We omit age and is_active, but the email error should be caught.

inspect_model(UserProfile, valid_user_data)
inspect_model(UserProfile, invalid_user_data)



