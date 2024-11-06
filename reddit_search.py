import aiohttp
import asyncio
from model import RedditPost
from datetime import datetime, timezone, timedelta

class RedditSearch:

    def __init__(self, subreddit_name: str):
        self.subreddit_name = subreddit_name
        self.url = f"https://www.reddit.com/{self.subreddit_name}/new.json"

    async def convert_utc_to_datetime(self, utc: int) -> datetime:
        return datetime.fromtimestamp(utc, tz=timezone.utc)
    
    async def validate_post_time(self, utc:int) -> bool:
        post_time = await self.convert_utc_to_datetime(utc)
        current_time = datetime.now(timezone.utc)
        return current_time - post_time <= timedelta(hours=2)

    async def search(self):
        async with aiohttp.ClientSession() as session:
            while True:
                headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
                async with session.get(self.url, headers=headers) as response:
                    if response.status == 429:
                        print("Rate limited. Retrying in 5 seconds")
                        await asyncio.sleep(5)  # Wait for 5 second before retrying
                        continue
                    data = await response.json()
                    # print(data)
                    posts = [
                        RedditPost
                        (
                            title=post["data"]["title"],
                            url=post["data"]["url"],
                            subreddit=self.subreddit_name,
                            text=post["data"]["selftext"],
                            post_id=post["data"]["id"],
                            created_utc=await self.convert_utc_to_datetime(post["data"]["created_utc"])
                        )
                        for post in data["data"]["children"]
                        if await self.validate_post_time(post["data"]["created_utc"])
                    ]
                    return posts
    




# async def main():
#     for i in range(0, 20):
#         reddit_search = RedditSearch("indiehackers")
#         posts = await reddit_search.search()
#         print(posts)
#         print(i)
#         print("=====================================")

# if __name__ == "__main__":
#     asyncio.run(main())