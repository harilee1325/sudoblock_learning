# --- Level 2: Solution ---
from typing import List
from pydantic import BaseModel
from practice import UserProfile
from practice import inspect_model
# (Assume UserProfile class from Level 1 is already defined)

class BlogPost(BaseModel):
    title: str
    content: str
    author: UserProfile # Nesting the model directly
    tags: List[str] = [] # Use List for arrays, default to empty list

# --- Test Cases ---
valid_post_data = {
    "title": "My First Post",
    "content": "Hello world!",
    "author": { # The nested object is just a dictionary
        "username": "charlie",
        "email": "charlie@web.com",
        "age": 30
    },
    "tags": ["pydantic", "python"]
}

invalid_post_data = {
    "title": "Invalid Post",
    "content": "This will fail.",
    "author": { # The nested object has an error
        "username": "dave"
        # Missing the required 'email' field for UserProfile
    }
}

inspect_model(BlogPost, valid_post_data)
inspect_model(BlogPost, invalid_post_data)