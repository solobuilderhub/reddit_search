from fastapi import FastAPI
from manage_subreddits import SubredditManager
from reddit_search import RedditSearch
from keyword_search import KeywordSearch

app = FastAPI()


@app.get("/")
async def read_root():
    subreddit_manager_obj = SubredditManager()
    subreddits = await subreddit_manager_obj.get_subreddits()
    subreddits_to_keywords = await subreddit_manager_obj.map_subreddits_keywords(subreddits)
    subreddits_to_email_keywords = await subreddit_manager_obj.map_subreddits_to_email_keywords(subreddits)

    for subreddit_keywords in subreddits_to_keywords:
        reddit_search = RedditSearch(subreddit_keywords.subreddit_name)
        posts = await reddit_search.search()

        # Search for keywords in posts
        keyword_search = KeywordSearch(subreddit_keywords.keywords, posts, subreddit_keywords.subreddit_name)
        keyword_search_result = keyword_search.search().result

        print("now searching for subreddit --> ", subreddit_keywords.subreddit_name)
        for email, keywords in subreddits_to_email_keywords[subreddit_keywords.subreddit_name].items():
            print(f"Keys are ---> {keywords}")
            for keys in keywords:
                if keys in keyword_search_result[subreddit_keywords.subreddit_name]:
                    print(f"Sending email to {email} -- {keys} --- post details -- {keyword_search_result[subreddit_keywords.subreddit_name][keys]}")
                    # Send email to email
                else:
                    print(f"Keyword {keys} not found in subreddit {subreddit_keywords.subreddit_name}")

    return {"msg": "okay"}


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