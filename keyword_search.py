import ahocorasick
from model import RedditPost, RedditSearchResult, KeywordResult

class KeywordSearch:

    def __init__(self, keywords: list, posts: list[RedditPost], subreddit: str):
        self._keywords = keywords
        self._A = ahocorasick.Automaton()
        self._posts = posts
        self._subreddit = subreddit
        self._search_res = {subreddit: {}}

        for idx, keyword in enumerate(keywords):
            self._A.add_word(keyword, (idx, keyword))
        self._A.make_automaton()

    def search(self) -> RedditSearchResult:
        found_post_ids = {}
        search_res = {self._subreddit: {}}
        for post in self._posts:
            for end_index, (idx, keyword) in self._A.iter(post.text):
                if keyword not in search_res[self._subreddit]:
                    search_res[self._subreddit][keyword] = KeywordResult(posts=[])
                post_detail = RedditPost(
                    title=post.title,
                    url=post.url,
                    subreddit=post.subreddit,
                    text=post.text,
                    post_id=post.post_id,
                    created_utc=post.created_utc
                )
                if post.post_id not in found_post_ids:
                    search_res[self._subreddit][keyword].posts.append(post_detail)
                    found_post_ids[post.post_id] = True
        return RedditSearchResult(result=search_res)

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

# # Example usage
# keywords = ["keyword1", "keyword2", "keyword3"]
# posts = [
#     RedditPost(
#         title="title",
#         url="url",
#         subreddit="r/fastapi",
#         text="keyword1 keyword3",
#         post_id="post_id",
#         created_utc=1694592693
#     ),
#     RedditPost(
#         title="title",
#         url="url",
#         subreddit="r/fastapi",
#         text="keyword1",
#         post_id="post_id",
#         created_utc=1694592693
#     ),
# ]

# keywords = ["keyword1", "keyword2", "keyword3"]
# searcher = KeywordSearch(keywords, posts, "r/fastapi")
# result = searcher.search()


# print("*********************")
# print(result)  # Output: {'keyword1': True, 'keyword2': False, 'keyword3': True}

# for keyword, keyword_result in result.subreddit["r/fastapi"].items():
#     print(keyword)
#     for post in keyword_result.posts:
#         print(post.text)
#         print(post.url)
#         print("=====================================")