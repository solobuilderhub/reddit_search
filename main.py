from fastapi import FastAPI
from manage_subreddits import SubredditManager

app = FastAPI()


@app.get("/")
async def read_root():
    await SubredditManager().get_subreddits()
    return {"msg": "okay"}

    