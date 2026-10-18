import httpx
import time
from fastapi import FastAPI

app=FastAPI()

JOKE_URL = "https://official-joke-api.appspot.com/random_joke"

@app.get("/jokes-sync")
def get_jokes_sync():
    start=time.time()
    jokes=[]
    with httpx.Client() as client:
        for _ in range(10):
            resp=client.get(JOKE_URL)
            data=resp.json()
            jokes.append(f"{data['setup']}: {data['punchline']}")
    elapsed=time.time() - start
    return{
        "mode":"sync",
        "elapsed_time":round(elapsed,3),
        "jokes":jokes
    }