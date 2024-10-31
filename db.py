from motor.motor_asyncio import AsyncIOMotorClient
from datetime import datetime, timedelta
import os
from model import Subreddit
from typing import List

class MongoDB:
    def __init__(self):
        self.client: AsyncIOMotorClient = None
        self.db = None

    async def connect_to_database(self):
        try:
            self.client = AsyncIOMotorClient(
                os.getenv("MONGODB_URL")
            )
            self.db = self.client.redditpulse
            self.collection = self.db.subreddits
            return self.db
        except Exception as e:
            print(f"Error connecting to database: {e}")
            raise e

    async def close_database_connection(self):
        if self.client:
            self.client.close()
            self.client = None
            self.db = None

    async def get_subreddits(self) -> List[Subreddit]:
        subreddits = []
        async for subreddit in self.collection.find():
            subreddit["_id"] = str(subreddit["_id"])  # Convert ObjectId to string
            subreddits.append(Subreddit(**subreddit))
        return subreddits