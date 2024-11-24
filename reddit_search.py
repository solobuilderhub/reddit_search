import aiohttp
import asyncio
from model import RedditPost
from datetime import datetime, timezone, timedelta
import os

class RedditSearch:

    def __init__(self, subreddit_name: str):
        self.subreddit_name = subreddit_name
        self.url = "https://reddit-scraper2.p.rapidapi.com/sub_posts"
        print("Now searching for subreddit: ", self.subreddit_name)
        self.querystring = {"sub": self.subreddit_name, "sort":"NEW"}
        self.headers = {
            "x-rapidapi-key": os.getenv("RAPID_API_KEY"),
            "x-rapidapi-host": "reddit-scraper2.p.rapidapi.com"
        }


    def convert_utc_to_datetime(self, date_str: str) -> datetime:
        if date_str == "":
            return None
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    

    async def validate_post_time(self, date_str:int) -> bool:
        if date_str == "":
            return False
        post_time = self.convert_utc_to_datetime(date_str)
        current_time = datetime.now(timezone.utc)
        return current_time - post_time <= timedelta(hours=6)


    async def search(self):
        async with aiohttp.ClientSession() as session:
            all_posts = []
            has_next_page = False
            cursor = None
            time = 0
            while True:
                if time == 3:
                    print("Reached max time limit")
                    return all_posts
            
                print("Wait 3 seconds before making a request")
                await asyncio.sleep(3)
                async with session.get(self.url, headers=self.headers, params=self.querystring) as response:
                    if response.status == 429:
                        print("Rate limited. Retrying in 5 seconds")
                        await asyncio.sleep(5)  # Wait for 5 second before retrying
                        continue

                    data = await response.json()
                    
                    post_data = data.get("data", [])
                    page_info = data.get("pageInfo", {})
                    has_next_page = page_info.get("hasNextPage", False)
                    cursor = page_info.get("endCursor", None)
                    print(f"total posts: {len(post_data)}")

                    for post in post_data:
                        print(f"Post: {post.get('title')}")
                        if await self.validate_post_time(post.get("creationDate", "")):
                            all_posts.append(
                                RedditPost(
                                    title=post.get("title", ""),
                                    url=post.get("url", ""),
                                    subreddit=self.subreddit_name,
                                    text=post.get("content").get("text", ""),
                                    post_id=post.get("id", ""),
                                    created_utc=self.convert_utc_to_datetime(post.get("creationDate", ""))
                                )
                            )
                        
                    if has_next_page:
                        print("Using cursor to get next page")
                        self.querystring["cursor"] = cursor
                        time += 1
                    else:
                        return all_posts
                    
    




# async def main():
#     reddit_search = RedditSearch("indiehackers")
#     posts = await reddit_search.search()
#     print(posts)
#     print(len(posts))
    

    # for i in range(0, 20):
    #     reddit_search = RedditSearch("indiehackers")
    #     posts = await reddit_search.search()
    #     print(posts)
    #     print(i)
    #     print("=====================================")

if __name__ == "__main__":
    asyncio.run(main())