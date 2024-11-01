from pydantic import BaseModel, Field, EmailStr
from typing import List, Dict
from bson import ObjectId
from datetime import datetime, timezone

# Pydantic model
class Subreddit(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    email: EmailStr
    subreddit_name: str
    keyword: List[str]



class IndividualSubredditKeywords(BaseModel):
    email: EmailStr
    keywords: List[str]


class SubredditEmailKeywords(BaseModel):
    subreddit_name: str
    individual_subreddits: List[IndividualSubredditKeywords]


class RedditPost(BaseModel):
    title: str
    url: str
    subreddit: str
    text: str
    post_id: str
    created_utc: datetime
 

class KeywordResult(BaseModel):
    keyword: List[RedditPost]

class RedditSearchResult(BaseModel):
    subreddit: Dict[str, KeywordResult]

