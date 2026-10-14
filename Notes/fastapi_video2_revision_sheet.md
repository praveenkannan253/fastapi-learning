# FastAPI Course: Video 2 Revision Sheet

> Note: The transcript has many missing words, so gaps are filled with standard content. The "POST Body Types" section is the most uncertain (transcript cuts off early). Verify against the video once.

Topics: FastAPI Basics, Decorator, Pydantic, GET and POST Method, POST Body Types

---

## 1. FastAPI Basics (Setup + First App)

**Setup steps:**
1. Install **Python** and a code editor (**VS Code**).
2. Create a **virtual environment**.
3. Install FastAPI and a server.
4. Write `main.py`, run it, open `/docs`.

**Virtual environment:** An isolated Python environment for one project, so its packages don't conflict with other projects.
- **Why:** Project A may need version 1 of a library and Project B version 2. A virtual env keeps them separate.
- **UV:** A fast Python package and environment manager (alternative to `pip` + `venv`).

```bash
uv venv                      # create virtual env
source .venv/bin/activate    # activate (Linux/Mac)
.venv\Scripts\activate       # activate (Windows)
uv pip install "fastapi[standard]"
```

**First app (`main.py`):**
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Hello, this is my first FastAPI app"}
```

**Run the server:**
```bash
fastapi dev main.py
# or
uvicorn main:app --reload
```

**Key terms:**
- **FastAPI():** creates the application object.
- **Uvicorn:** an **ASGI server** that actually runs your app and listens for requests.
- **`--reload`:** server restarts automatically whenever you save the file. Use it only in **development**, not production.
- **Default port:** **8000** (`http://127.0.0.1:8000`).
- **Starlette:** handles the HTTP part (requests, responses, routing). FastAPI is built on top of it.
- **Pydantic:** handles data validation.

**Auto docs:**
| URL | What it is |
|-----|------------|
| `/docs` | **Swagger UI** (interactive, you can test endpoints) |
| `/redoc` | **ReDoc** (clean read-only documentation) |
| `/openapi.json` | **OpenAPI specification** (JSON file describing your whole API; Swagger reads this) |

**OpenAPI:** A standard format to describe REST APIs. FastAPI generates it automatically from your code.

---

## 2. Decorator (Python concept)

**Decorator:** A function that takes another function, **adds extra behaviour** to it, and returns the modified function, **without changing the original code**.

**Real-world example (Pizza):**
- Plain pizza = the **existing function**.
- Toppings (cheese, olives) = the **decorator**.
- You don't remake the pizza. You just add toppings on top, and now it's a "modified pizza".

```python
def add_toppings(func):            # decorator
    def wrapper():
        print("Adding cheese...")  # extra behaviour (before)
        func()                     # original function runs
        print("Adding olives...")  # extra behaviour (after)
    return wrapper

@add_toppings
def plain_pizza():
    print("Plain pizza is ready")

plain_pizza()
```

Output:
```
Adding cheese...
Plain pizza is ready
Adding olives...
```

**Important points:**
- `@add_toppings` above a function is the same as `plain_pizza = add_toppings(plain_pizza)`.
- **Functions are first-class objects** in Python, so they can be passed as arguments and returned from other functions. This is why decorators work.
- **In FastAPI:** `@app.get("/")` is a decorator. It registers your function as the handler for `GET /`.

---

## 3. Pydantic (Data Validation)

**Pydantic:** A Python library for **data validation** using **type hints**. It checks that incoming data has the correct types and format.

**Real-world example:** Like an **ID proof check** at the airport. If the details don't match the rules, you are not allowed in.

**Why needed:** Anything coming from outside (user input, API requests, files) can't be trusted. Validate before use. This is also important in ML/AI pipelines for clean data.

```python
from pydantic import BaseModel, EmailStr

class User(BaseModel):
    name: str
    age: int
    email: EmailStr
```

> `EmailStr` needs the `email-validator` package. It is included with `fastapi[standard]`.

**Valid data:**
```python
user = User(name="Praveen", age=22, email="praveen@gmail.com")
```

**Invalid data (errors):**
```python
User(name=123, age=22, email="praveen@gmail.com")
# Input should be a valid string

User(name="Praveen", age=22, email="praveen.com")
# value is not a valid email address
```

**Key terms:**
- **BaseModel:** the base class. Inherit from it to create a data model (schema).
- **Schema / Data model:** defines the fields and their types.
- **Type coercion:** Pydantic tries to convert compatible values. Example: `"22"` becomes `22` for an `int` field. If conversion fails, it raises a **ValidationError**.
- In FastAPI, a validation failure returns **422 Unprocessable Entity** automatically.

---

## 4. GET and POST Method

**Recap:**
- **GET:** read data. **POST:** create data. Both are the most commonly used HTTP methods.

**Example: Users API**

```python
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI()

class User(BaseModel):
    name: str
    age: int
    hobbies: List[str]          # list of strings

class UserResponse(BaseModel):  # what we send back
    name: str
    age: int

users = []                      # temporary in-memory "database"

@app.get("/users/{user_id}", response_model=UserResponse)
def get_user(user_id: int):
    if user_id >= len(users):
        raise HTTPException(status_code=404, detail="User not found")
    return users[user_id]

@app.post("/users", status_code=201)
def create_user(user: User):
    users.append(user.model_dump())
    return {"message": "User created", "user": user}
```

**Key terms:**
- **Path parameter:** value inside the URL path. Example: `/users/{user_id}`. The type hint `int` auto-validates it.
- **Query parameter:** value after `?` in the URL. Example: `/users?age=22`. Function params not in the path become query params.
- **Request body:** data sent in the POST body. In FastAPI, a parameter typed as a **Pydantic model** is read from the body.
- **response_model:** controls what the API returns. It filters fields (example: hides password) and documents the output in Swagger.
- **`List[str]`:** a list of strings. Import from `typing` (or use `list[str]` in Python 3.9+).
- **HTTPException:** used to return an error response with a status code and message.
- **status_code=201:** correct code for successful creation.

**Tip:** Test both endpoints in `/docs` using the "Try it out" button.

---

## 5. POST Body Types

The request body can be sent in different formats. The **Content-Type** header tells the server which format it is.

| Body Type | Content-Type | Used for |
|-----------|--------------|----------|
| **JSON** | `application/json` | Most common for APIs. Structured data. |
| **Text** | `text/plain` | Simple plain text data. |
| **Form data** | `application/x-www-form-urlencoded` | HTML forms, example: username and password in a login form. |
| **Multipart form data** | `multipart/form-data` | File uploads (images, PDFs). |

**JSON body (most common):**
```python
@app.post("/users")
def create_user(user: User):   # Pydantic model, so JSON body
    return user
```

**Form data:**
```python
from fastapi import Form

@app.post("/login")
def login(username: str = Form(...), password: str = Form(...)):
    return {"username": username}
```
> Form support needs the `python-multipart` package (included in `fastapi[standard]`).

**Important points:**
- **JSON** is used for API-to-API or app-to-API communication.
- **Form data** is used mainly for browser HTML forms (login pages).
- Never send passwords in the URL (GET). Always use the POST body.

---

## Quick Revision Points
1. Use a **virtual environment** per project. **UV** is a fast tool for it.
2. Run with `fastapi dev main.py` or `uvicorn main:app --reload`. Default port **8000**.
3. `/docs` = Swagger, `/redoc` = ReDoc, `/openapi.json` = OpenAPI spec.
4. **Decorator** = function that adds behaviour to another function. `@app.get()` is one.
5. **Pydantic BaseModel** validates data using type hints. Failure gives **422**.
6. **Path param** is in the URL path, **query param** is after `?`, **body** is in POST.
7. **response_model** controls and documents the output.
8. Body types: **JSON**, **text**, **form data**, **multipart (files)**.

---

## Interview Q&A

**Q1. What is a decorator in Python?**
A: A function that wraps another function to add extra behaviour without modifying its code. Example: `@app.get("/")` in FastAPI.

**Q2. What is Pydantic and why does FastAPI use it?**
A: Pydantic is a data validation library based on type hints. FastAPI uses it to validate request data automatically and to generate schema documentation.

**Q3. What is the difference between path parameters and query parameters?**
A: Path parameters are part of the URL path (`/users/5`) and identify a specific resource. Query parameters come after `?` (`/users?age=22`) and are used for filtering or optional values.

**Q4. What does `--reload` do in uvicorn?**
A: It restarts the server automatically when code changes. It is meant for development only.

**Q5. What is `response_model` in FastAPI?**
A: It defines the shape of the response. It filters out extra fields (like passwords) and shows the output schema in Swagger docs.

**Q6. What is the difference between Uvicorn and FastAPI?**
A: FastAPI is the web framework where you write your logic. Uvicorn is the ASGI server that runs the app and handles network connections.

**Q7. What happens if the request data fails Pydantic validation?**
A: FastAPI automatically returns **422 Unprocessable Entity** with details about which field failed.

**Q8. When do you use JSON body vs form data?**
A: JSON for API clients and apps (structured data). Form data for HTML browser forms like login pages. Multipart form data when uploading files.

**Q9. Why use a virtual environment?**
A: To isolate project dependencies so that different projects with different package versions don't conflict.
