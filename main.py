from fastapi import FastAPI
from manage_subreddits import SubredditManager
from reddit_search import RedditSearch
from keyword_search import KeywordSearch
from model import EmailRedditPost, SendEmail
from email_service import EmailService

app = FastAPI()


@app.get("/")
async def read_root():
    email_post = {}
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


        for email, keywords in subreddits_to_email_keywords[subreddit_keywords.subreddit_name].items():
            for keys in keywords:
                if keys in keyword_search_result[subreddit_keywords.subreddit_name]:
                    found_posts = keyword_search_result[subreddit_keywords.subreddit_name][keys].posts

                    for post in found_posts:
                        email_post_model = EmailRedditPost(
                            url=post.url,
                            text=post.text,
                            title=post.title,
                            keyword=keys,
                            subreddit=subreddit_keywords.subreddit_name
                        )
                        if email in email_post:
                            email_post[email].append(email_post_model)
                        else:
                            email_post[email] = [email_post_model]
                    # Send email to email
                else:
                    print(f"Keyword {keys} not found in subreddit {subreddit_keywords.subreddit_name}")


    # now send email to all the emails after processing the model
    for email, posts in email_post.items():
        print(f"Sending email to {email} with posts {posts}")
        send_email_model = SendEmail(email=email, posts=posts)
        # Send email to email
        email_service = EmailService(send_email_model)
        response = email_service.send_email()

    print("Script Run Successfully")
    return {"msg": "Script Run Successfully"}


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