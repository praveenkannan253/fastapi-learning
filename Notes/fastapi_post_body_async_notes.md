# FastAPI Revision Sheet: POST Body Types + Async/Await

> Source: YouTube video https://youtu.be/DRPpaFNpS-8
> Note: the transcript was very garbled, so this sheet is reconstructed from the topics and keywords in it. Run every example yourself to confirm.

---

## Part 1: POST Request Body Types

### What is a request body?
The **request body** is the data the client sends *inside* the HTTP request (not in the URL). It is used with POST, PUT and PATCH. The **Content-Type** header tells the server what format the body is in.

### The 4 types covered

| # | Body type | Content-Type header | FastAPI tool | Real-world example |
|---|-----------|--------------------|--------------|--------------------|
| 1 | JSON | `application/json` | Pydantic `BaseModel` | Mobile app sending a new order to a backend |
| 2 | Plain text | `text/plain` | `Request` / `Body(media_type=...)` | Sending a raw note or log line |
| 3 | Form data | `application/x-www-form-urlencoded` | `Form(...)` | Browser login form (username + password) |
| 4 | File upload | `multipart/form-data` | `UploadFile`, `File(...)` | Uploading a PDF or profile photo |

### Key points to remember
- **JSON** is the default and most common for APIs.
- **Form data** needs the package `python-multipart` installed. Without it FastAPI raises an error.
- **Multipart** is used when a file is sent (it can also carry normal form fields together with the file).
- You cannot mix a JSON body and Form fields in the same endpoint. HTTP allows only one body format per request.
- `UploadFile` is better than `bytes` for big files: it uses a spooled file, so memory stays low.

---

## Part 2: Async / Await

### Synchronous vs Asynchronous
- **Synchronous**: one task at a time. Task 2 waits until Task 1 finishes.
- **Asynchronous**: while one task is *waiting* (for network, database, disk), the program starts other tasks.

**Real-world example:** A cook who puts rice on the stove and, while it cooks, chops vegetables. He does not stand and stare at the rice. That is async.

### Important terms
- **`async def`**: defines a coroutine function.
- **`await`**: pause here, let others run, come back when the result is ready.
- **Coroutine**: the object returned by calling an `async def` function.
- **Event loop**: the manager that switches between waiting tasks.
- **`asyncio.gather()`**: runs many coroutines concurrently and returns a list of results.
- **Unpacking operator `*`**: spreads a list into separate arguments, so `gather(*tasks)`.
- **I/O-bound task**: a task that mostly waits (API calls, DB). Async helps here.
- **CPU-bound task**: a task that mostly computes. Async does NOT help here.

### FastAPI behaviour
- If your endpoint is `def` (normal), FastAPI runs it in a **thread pool**.
- If your endpoint is `async def`, FastAPI runs it directly on the **event loop**.
- Inside `async def`, never use a blocking library like `requests`. It blocks the whole event loop. Use **`httpx`** (async client) instead.

### Demo result from the video (approximate)
Calling a public jokes API **10 times**:
- Synchronous (`requests`, one by one): about **4.4 seconds**
- Asynchronous (`httpx` + `asyncio.gather`): about **0.8 seconds**

That is roughly 5x faster, because the 10 calls wait together instead of one after another.

---

## Part 3: Practice Code

### Setup
```bash
python -m venv venv
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

pip install fastapi "uvicorn[standard]" python-multipart httpx requests
```

### File: `main.py`  (POST body types)
```python
from fastapi import FastAPI, Request, Form, File, UploadFile
from pydantic import BaseModel

app = FastAPI()


# ---------- 1. JSON body ----------
class Item(BaseModel):
    name: str
    price: float
    in_stock: bool = True


@app.post("/json")
async def json_body(item: Item):
    return {"received": item, "total_with_gst": round(item.price * 1.18, 2)}


# ---------- 2. Plain text body ----------
@app.post("/text")
async def text_body(request: Request):
    raw = await request.body()          # bytes
    return {"text": raw.decode("utf-8")}


# ---------- 3. Form data (URL-encoded) ----------
@app.post("/login")
async def login(username: str = Form(...), password: str = Form(...)):
    # Never return a password in real apps. Only for learning.
    return {"username": username, "password_length": len(password)}


# ---------- 4. File upload (multipart) ----------
@app.post("/upload")
async def upload(file: UploadFile = File(...)):
    content = await file.read()
    return {
        "filename": file.filename,
        "content_type": file.content_type,
        "size_bytes": len(content),
    }
```

Run it:
```bash
uvicorn main:app --reload
```
Open `http://127.0.0.1:8000/docs` (Swagger UI) to test.

### Test with curl
```bash
# JSON
curl -X POST http://127.0.0.1:8000/json \
  -H "Content-Type: application/json" \
  -d '{"name":"Pen","price":10.5}'

# Plain text
curl -X POST http://127.0.0.1:8000/text \
  -H "Content-Type: text/plain" \
  -d "Hi everyone"

# Form data
curl -X POST http://127.0.0.1:8000/login \
  -d "username=praveen&password=secret123"

# File upload
curl -X POST http://127.0.0.1:8000/upload \
  -F "file=@sample.pdf"
```

### File: `async_demo.py`  (sync vs async comparison)
```python
import time
import asyncio
import requests
import httpx
from fastapi import FastAPI

app = FastAPI()

JOKE_URL = "https://official-joke-api.appspot.com/random_joke"


# ---------- Synchronous: one by one ----------
@app.get("/jokes-sync")
def jokes_sync():
    start = time.perf_counter()
    jokes = []
    for _ in range(10):
        r = requests.get(JOKE_URL)          # blocks here each time
        jokes.append(r.json())
    return {"seconds": round(time.perf_counter() - start, 2), "count": len(jokes)}


# ---------- Asynchronous: all together ----------
async def fetch_joke(client: httpx.AsyncClient):
    r = await client.get(JOKE_URL)
    return r.json()


@app.get("/jokes-async")
async def jokes_async():
    start = time.perf_counter()
    async with httpx.AsyncClient() as client:
        tasks = [fetch_joke(client) for _ in range(10)]   # list comprehension
        jokes = await asyncio.gather(*tasks)              # * unpacks the list
    return {"seconds": round(time.perf_counter() - start, 2), "count": len(jokes)}
```

Run it:
```bash
uvicorn async_demo:app --reload
```
Then hit `/jokes-sync` and `/jokes-async` and compare the `seconds` value.

### Why `*tasks`?
`gather` expects separate arguments: `gather(t1, t2, t3)`.
You have a list `[t1, t2, t3]`, so `*` unpacks it into `t1, t2, t3`.

---

## Part 4: Interview Q&A (with answers)

**Q1. What are the common request body types in FastAPI?**
A. JSON (Pydantic model), plain text, URL-encoded form data (`Form`), and multipart file upload (`UploadFile`).

**Q2. Which package is required for Form and File uploads?**
A. `python-multipart`.

**Q3. Difference between `application/x-www-form-urlencoded` and `multipart/form-data`?**
A. URL-encoded is for simple key-value fields (like a login form). Multipart is for files, and can also carry normal fields.

**Q4. Why prefer `UploadFile` over `bytes` for files?**
A. It uses a spooled temporary file, so large files do not sit fully in memory. It also gives `filename` and `content_type`.

**Q5. When should I use `async def` vs `def` in FastAPI?**
A. Use `async def` when you `await` async libraries (httpx, async DB drivers). Use plain `def` when calling blocking libraries; FastAPI runs those in a thread pool.

**Q6. Why is `requests` bad inside an `async def` endpoint?**
A. It is blocking, so it freezes the event loop and every other request waits.

**Q7. What does `asyncio.gather` do?**
A. Runs multiple coroutines concurrently and returns their results as a list, in the same order.

**Q8. Does async make CPU-heavy code faster?**
A. No. It helps only I/O-bound work. For CPU-bound work use multiprocessing or a worker queue.

---

## Part 5: Git Workflow to Update Your Repo

```bash
cd your-repo
mkdir fastapi-basics
# copy main.py, async_demo.py, and this notes file into fastapi-basics/

pip freeze > requirements.txt     # or write only the 5 packages by hand

git add .
git commit -m "Add FastAPI POST body types and async/await practice"
git push origin main
```

Suggested repo layout:
```
fastapi-basics/
  main.py
  async_demo.py
  requirements.txt
  NOTES.md
```

Add a `.gitignore` with `venv/` and `__pycache__/` before your first commit.

---

## Quick Revision Checklist
- [ ] I can explain the 4 body types and their Content-Type headers
- [ ] I installed `python-multipart` and tested Form + File in Swagger
- [ ] I ran sync vs async and saw the time difference myself
- [ ] I can explain `gather(*tasks)` in one sentence
- [ ] Code is pushed to GitHub
