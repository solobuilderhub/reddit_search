from pydantic import BaseModel, Field, EmailStr
from typing import List
from bson import ObjectId


# Pydantic model
class Subreddit(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    subreddit_name: str
    keyword: List[str]
