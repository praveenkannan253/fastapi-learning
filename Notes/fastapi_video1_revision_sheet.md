# FastAPI Course: Video 1 Revision Sheet

> Note: The transcript had many missing words, so some gaps are filled with standard content. Verify against the video once.

Source: https://youtu.be/DRPpaFNpS-8

---

## 1. REST API Intro

**API (Application Programming Interface):** A set of rules that lets one software talk to another software.

**Real-world example:** In a restaurant, you (client) don't go into the kitchen. The waiter (API) takes your order to the kitchen (server) and brings the food (response) back.

**Client-Server flow:**
```
Client (Browser/App)  --Request-->  API/Backend  --Query-->  Database
Client (Browser/App)  <--Response-- API/Backend  <--Data---  Database
```

**REST (Representational State Transfer):** An architectural style for designing APIs over HTTP. Data is treated as **resources**, and each resource has a **URL**.

**Why an API is needed:**
- **Separation:** The user interface (frontend) and the backend are independent. The same API can serve a website, an Android app, and an iOS app.
- **Data validation:** The backend checks incoming data before saving it. Example: age must be a number, email must be in a valid format. Wrong data gets rejected with an error.
- **Security:** The frontend never touches the database directly.

**Parts of a request:**
- **URL / Endpoint:** the address. Example: `https://api.flipkart.com/products`
  - `api.flipkart.com` is the **base URL (domain)**
  - `/products` is the **endpoint (path)**
- **HTTP Method:** the action (GET, POST, etc.)
- **Headers:** metadata (content type, authentication token)
- **Request Payload (Body):** the data sent to the server, usually in **JSON**
- **Response:** data plus a **status code**

**JSON example (payload):**
```json
{ "username": "praveen", "password": "abc123" }
```

---

## 2. FastAPI History

| Year | Event |
|------|-------|
| 1991 | **Python** created by Guido van Rossum. It is open source. |
| 2005 | **Django** released. Full-stack framework following the **MVC (Model-View-Controller)** pattern. "Batteries included" (ORM, admin, auth). |
| 2010 | **Flask** released by Armin Ronacher. A **micro-framework**, inspired by **Sinatra** (a Ruby framework). Minimal core, you add what you need. |
| 2015 | **OpenAPI / Swagger** standard for describing REST APIs. |
| 2018 | **FastAPI** released by Sebastián Ramírez. |

**Key terms:**
- **Full-stack framework (Django):** gives everything built in. Heavy, but structured.
- **Micro-framework (Flask):** lightweight, flexible, but you add validation, docs, etc. yourself.
- **FastAPI:** built on top of **Starlette** (web layer) and **Pydantic** (data validation). It uses Python **type hints**.

**Idea:** FastAPI took the good parts (Flask's simplicity, Django's features) and added speed plus automatic documentation.

---

## 3. Why FastAPI?

**Reason 1: High performance (Concurrency)**
- Flask and Django traditionally run **synchronously (WSGI)**. One request waits until the previous task (like a DB call) finishes.
- FastAPI is **asynchronous (ASGI)** and supports `async` / `await`.
- **Concurrency:** handling many tasks by switching between them while one is waiting.
- **Example:** A chef who puts rice on the stove and chops vegetables while it cooks, instead of staring at the rice until it's done.
- Result: faster handling of many requests, especially **I/O-bound** work (database, network calls).

**Reason 2: Automatic documentation**
- Swagger UI at `/docs`
- ReDoc at `/redoc`
- You can test your API in the browser itself. No Postman needed for basic testing.

**Reason 3: Data validation + type hints**
- Uses **Pydantic**. Define a model once, and validation and errors come automatically.
- Fewer bugs, better editor autocomplete.

**Reason 4: Easy to learn, less code**

---

## 4. HTTP Methods

**HTTP (HyperText Transfer Protocol):** the protocol clients and servers use to communicate. **HTTPS** is the secure version (encrypted).

**Running example: a Books API** (`/books`)

| Method | Purpose (CRUD) | Example |
|--------|----------------|---------|
| **GET** | **Read** data | `GET /books` returns the list of books. `GET /books/1` returns one book. |
| **POST** | **Create** new data | `POST /books` with a JSON body adds a new book. |
| **PUT** | **Update** (replace the whole record) | `PUT /books/1` replaces the full record for book 1. |
| **PATCH** | **Partial update** (only some fields) | `PATCH /books/1` changes only the price. |
| **DELETE** | **Remove** data | `DELETE /books/1` deletes book 1. |

**Important points:**
- **GET** has no body. Data goes in the URL. **POST** carries data in the request body.
- **POST example:** Login or sign-up, where username and password are sent in the body (not visible in the URL).
- **PUT vs PATCH:** PUT updates **all** fields, PATCH updates **only the given** fields.
- If you use the wrong method on an endpoint, you get **405 Method Not Allowed**.
- **Idempotent:** the same request repeated gives the same result. GET, PUT, DELETE are idempotent. POST is not (it creates a new record each time).

**Example (PUT):** The existing record is "Harry Potter Part 1". You send new data, and the existing record gets modified.

---

## 5. HTTP Status Codes

| Series | Meaning | Common codes |
|--------|---------|--------------|
| **1xx** | Informational | 100 Continue |
| **2xx** | **Success** | **200 OK**, **201 Created** (POST success), **204 No Content** (DELETE success) |
| **3xx** | **Redirection** | 301 Moved Permanently, 304 Not Modified |
| **4xx** | **Client error** (your mistake) | **400 Bad Request**, **401 Unauthorized**, **403 Forbidden**, **404 Not Found**, **405 Method Not Allowed**, **422 Unprocessable Entity** (FastAPI validation error) |
| **5xx** | **Server error** (server's mistake) | **500 Internal Server Error**, 502 Bad Gateway, 503 Service Unavailable |

**Memory trick:**
- 2xx = All good
- 3xx = Go somewhere else
- 4xx = You messed up
- 5xx = Server messed up

---

## Quick Revision Points
1. API = a messenger between client and server.
2. REST = resources + URLs + HTTP methods.
3. Flask (2010, micro) → FastAPI (2018, modern, async).
4. FastAPI = fast + auto docs (`/docs`) + Pydantic validation.
5. CRUD = POST, GET, PUT/PATCH, DELETE.
6. Status codes: 2xx success, 4xx client error, 5xx server error.

---

## Interview Q&A

**Q1. What is a REST API?**
A: An API that follows REST principles. It exposes resources through URLs and uses HTTP methods (GET, POST, PUT, DELETE) for operations, usually exchanging JSON.

**Q2. Difference between Flask and FastAPI?**
A: Flask is synchronous by default and has no built-in validation or auto docs. FastAPI is asynchronous (ASGI), uses Pydantic for validation, and generates Swagger docs automatically.

**Q3. What is the difference between PUT and PATCH?**
A: PUT replaces the entire resource. PATCH updates only the specified fields.

**Q4. What does status code 404 vs 500 mean?**
A: 404 means the resource was not found (client side issue). 500 means an unexpected error on the server.

**Q5. What is concurrency, and why does FastAPI benefit from it?**
A: Concurrency is handling multiple tasks by switching while one waits (for example on a DB call). FastAPI's `async` support lets it serve many requests efficiently.

**Q6. Is POST idempotent?**
A: No. Repeating a POST can create duplicate records. GET, PUT, and DELETE are idempotent.
