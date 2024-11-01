from db import MongoDB
from typing import List
from model import Subreddit, SubredditKeywords, SubredditEmailKeywords, IndividualSubredditKeywords

db = MongoDB()


class SubredditManager:

    async def get_subreddits(self) -> List[Subreddit]:
        await db.connect_to_database()
        subreddits = await db.get_subreddits()
        await db.close_database_connection()
        await self.map_subreddits_keywords(subreddits)
        await self.map_subreddits_to_email_keywords(subreddits)
        return subreddits
    
    async def map_subreddits_keywords(self, subreddits: List[Subreddit]) -> List[SubredditKeywords]:
        subreddits_dict = {}

        for subreddit in subreddits:
            if subreddit.subreddit_name not in subreddits_dict:
                subreddits_dict[subreddit.subreddit_name] = set(subreddit.keyword)
            else:
                subreddits_dict[subreddit.subreddit_name].update(subreddit.keyword)

        # Convert sets to lists and create SubredditKeywords objects
        subreddit_keywords_list = [
            SubredditKeywords(subreddit_name=k, keywords=list(v))
            for k, v in subreddits_dict.items()
        ]
        print(subreddit_keywords_list)
        return subreddit_keywords_list
    
    async def map_subreddits_to_email_keywords(self, subreddits: List[Subreddit]) -> SubredditEmailKeywords:
        subreddits_dict = {}
        
        for subreddit in subreddits:
            if subreddit.subreddit_name not in subreddits_dict:
                subreddits_dict[subreddit.subreddit_name] = {subreddit.email: set(subreddit.keyword)}
            else:
                if subreddit.email not in subreddits_dict[subreddit.subreddit_name]:
                    subreddits_dict[subreddit.subreddit_name][subreddit.email] = set(subreddit.keyword)
                else:
                    subreddits_dict[subreddit.subreddit_name][subreddit.email].update(subreddit.keyword)
        
        # Convert sets to lists and create SubredditEmailKeywords objects
        email_keywords_dict = {}
        for k, v in subreddits_dict.items():
            individual_subreddits = []

            for email, keywords in v.items():
                individual_subreddits.append(IndividualSubredditKeywords(email=email, keywords=list(keywords)))
            email_keywords_dict[k] = individual_subreddits

        subreddit_email_keywords_list = []
        for k, v in email_keywords_dict.items():
            subreddit_email_keywords_list.append(SubredditEmailKeywords(subreddit_name=k, individual_subreddits=v))

        print(subreddit_email_keywords_list)
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
#         "email": ["keyword"],
#         "email2": ["keyword", "keyword2", "keyword3"],
#     },
#     "r/hacker": {
#         "email": ["keyword"],
#         "email2": ["keyword", "keyword2", "keyword3"],
#     }
# }

# {
#     'r/fastapi': [
#         'api', 
#         'database', 
#         'models'
#     ]
# } # done