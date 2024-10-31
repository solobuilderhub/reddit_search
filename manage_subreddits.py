from db import MongoDB
from typing import List
from model import Subreddit

db = MongoDB()


class SubredditManager:

    async def get_subreddits(self) -> List[Subreddit]:
        await db.connect_to_database()
        subreddits = await db.get_subreddits()
        await db.close_database_connection()
        await self.map_subreddits_keywords(subreddits)
        await self.map_subreddits_to_email_keywords(subreddits)
        return subreddits
    
    async def map_subreddits_keywords(self, subreddits: List[Subreddit]) -> dict[str, List[str]]:
        subreddits_dict = {}

        for subreddit in subreddits:
            if subreddit.subreddit_name not in subreddits_dict:
                subreddits_dict[subreddit.subreddit_name] = set(subreddit.keyword)
            else:
                subreddits_dict[subreddit.subreddit_name].update(subreddit.keyword)
        return subreddits_dict
    
    async def map_subreddits_to_email_keywords(self, subreddits: List[Subreddit]) -> dict[str, List[str]]:
        subreddits_dict = {}
        

        for subreddit in subreddits:
            if subreddit.subreddit_name not in subreddits_dict:
                subreddits_dict[subreddit.subreddit_name] = {subreddit.email: set(subreddit.keyword)}
            else:
                if subreddit.email not in subreddits_dict[subreddit.subreddit_name]:
                    subreddits_dict[subreddit.subreddit_name][subreddit.email] = set(subreddit.keyword)
                else:
                    subreddits_dict[subreddit.subreddit_name][subreddit.email].update(subreddit.keyword)
        
        return subreddits_dict



# {
#     "r/fastapi": {
#         "keyword": [
#             {
#                 "post_url": "",
#                 "text": ""
#             }
#         ]
#     }
# }



# {
#     "f/fastapi": {
#         "email": ["keyword"]
#     }
# }

# {
#     'r/fastapi': {
#         'api', 
#         'database', 
#         'models'
#     }
# } # done