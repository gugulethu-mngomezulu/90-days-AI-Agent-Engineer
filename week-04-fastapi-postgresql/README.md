# 🚀 Week 04 - FastAPI & PostgreSQL

## 90 Days of AI Agent Engineering

**Level:** Developing

Week 4 focuses on understanding how Python becomes a real backend service.

In Week 3, I learned how Python can communicate with external APIs using HTTP requests, `async/await`, `httpx`, concurrency, timeouts and error handling.

Now I am moving to the other side of that communication.

Instead of only asking:

> How does my Python application call an API?

I now want to understand:

> How do I build the API that receives the request?

This week focuses on:

- FastAPI
- HTTP routing
- Request and response flow
- Pydantic
- Data validation
- CRUD
- PostgreSQL
- Database connections
- SQL
- ORM concepts
- SQLAlchemy
- Database migrations
- Alembic
- Dependency Injection
- Error handling
- API testing
- Async backend concepts

---

# 🧠 1. What is a Backend?

A backend is the part of an application responsible for things such as:

- Business logic
- Processing requests
- Authentication
- Database communication
- Data validation
- Calling external services
- Running AI models or agents
- Returning responses to clients

A simple architecture might look like:

```text
Frontend
   │
   │ HTTP Request
   ↓
FastAPI Backend
   │
   ├── Validate Data
   ├── Run Business Logic
   ├── Call External APIs
   └── Read / Write Database
             │
             ↓
         PostgreSQL
             │
             ↓
FastAPI Response
   │
   ↓
Frontend
```

The frontend does not normally communicate directly with the database.

The backend sits between the client and the database.

---

# ⚡ 2. What is FastAPI?

FastAPI is a Python web framework used for building APIs.

It allows Python functions to become HTTP endpoints.

A basic FastAPI application:

```python
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def home():
    return {"message": "API is running"}
```

Here:

```python
app = FastAPI()
```

creates the FastAPI application.

This:

```python
@app.get("/")
```

creates a route.

And:

```python
def home():
```

is the Python function that runs when that route receives a request.

The result:

```json
{
  "message": "API is running"
}
```

is returned to the client.

---

# 🌐 3. Understanding HTTP

FastAPI works using HTTP.

HTTP allows clients and servers to communicate.

For example:

```text
Browser / App
      │
      │ GET /notes
      ↓
FastAPI Server
      │
      │ JSON Response
      ↓
Browser / App
```

An HTTP request can contain:

- HTTP method
- URL
- Headers
- Query parameters
- Path parameters
- Request body

The server processes that request and returns an HTTP response.

---

# 🛣️ 4. HTTP Methods

The most common methods are:

```text
GET
POST
PUT
PATCH
DELETE
```

They commonly map to CRUD operations.

```text
CRUD       HTTP

Create  →  POST
Read    →  GET
Update  →  PUT / PATCH
Delete  →  DELETE
```

Example Developer Notes API:

```text
POST   /notes
GET    /notes
GET    /notes/1
PUT    /notes/1
DELETE /notes/1
```

---

# 🟢 5. GET

`GET` retrieves information.

Example:

```python
@app.get("/notes")
def get_notes():
    return notes
```

Request:

```text
GET /notes
```

Response:

```json
[
  {
    "id": 1,
    "title": "FastAPI",
    "content": "Learning FastAPI"
  }
]
```

A GET request should generally retrieve data rather than modify it.

---

# 🔵 6. POST

`POST` creates something.

Example:

```python
@app.post("/notes")
def create_note(note: Note):
    return note
```

The client might send:

```json
{
  "title": "Async Python",
  "content": "Learning async and await"
}
```

FastAPI receives the data and passes it into the function.

---

# 🟡 7. PUT and PATCH

Both are used for updates, but conceptually they are slightly different.

`PUT` normally represents replacing the full resource.

```text
PUT /notes/1
```

`PATCH` normally represents changing only part of it.

```text
PATCH /notes/1
```

Example:

```json
{
  "title": "Updated FastAPI Notes"
}
```

---

# 🔴 8. DELETE

DELETE removes a resource.

```text
DELETE /notes/1
```

The backend finds note `1` and removes it.

---

# 📍 9. Path Parameters

Sometimes information forms part of the URL.

Example:

```text
/notes/10
```

Here:

```text
10
```

is the ID of the note.

FastAPI:

```python
@app.get("/notes/{note_id}")
def get_note(note_id: int):
    return {"note_id": note_id}
```

If the request is:

```text
GET /notes/10
```

then:

```python
note_id
```

becomes:

```text
10
```

---

# 🔎 10. Query Parameters

Query parameters usually appear after `?`.

Example:

```text
GET /notes?category=python
```

FastAPI:

```python
@app.get("/notes")
def get_notes(category: str | None = None):
    return {"category": category}
```

They are useful for:

- Filtering
- Searching
- Sorting
- Pagination

For example:

```text
/notes?category=python

/notes?limit=10

/notes?search=fastapi

/notes?page=2
```

---

# 📦 11. Request Body

POST, PUT and PATCH requests often send data inside the request body.

Example:

```json
{
  "title": "FastAPI Notes",
  "content": "Learning backend development",
  "category": "Python"
}
```

The backend needs to know what structure it expects.

This is where Pydantic becomes important.

---

# ✅ 12. What is Pydantic?

Pydantic provides data validation using Python type hints.

Example:

```python
from pydantic import BaseModel


class NoteCreate(BaseModel):
    title: str
    content: str
    category: str
```

Then:

```python
@app.post("/notes")
def create_note(note: NoteCreate):
    return note
```

FastAPI knows that the request should contain:

```text
title    → string
content  → string
category → string
```

If incorrect data is sent, FastAPI/Pydantic can reject it before the data reaches the rest of the application.

---

# 🛡️ 13. Why Validation Matters

Imagine the backend expects:

```json
{
  "title": "FastAPI",
  "content": "My notes",
  "category": "Python"
}
```

But receives invalid or missing data.

Without validation, bad data could reach:

```text
Application Logic
        ↓
Database
```

With validation:

```text
Request
   ↓
Pydantic
   ↓
Is data valid?
   │
   ├── YES → Continue
   │
   └── NO → Validation Error
```

Validation creates a boundary between external input and application logic.

---

# 🔄 14. CRUD

CRUD stands for:

```text
C → Create
R → Read
U → Update
D → Delete
```

Almost every backend system performs some form of CRUD.

For the Developer Notes API:

```text
CREATE

POST /notes

        ↓

Create new note
```

```text
READ

GET /notes

        ↓

Return notes
```

```text
UPDATE

PUT /notes/1

        ↓

Update note 1
```

```text
DELETE

DELETE /notes/1

        ↓

Delete note 1
```

---

# 🗄️ 15. What is a Database?

A database stores information persistently.

Without a database, I could do:

```python
notes = []
```

But that data lives in the application's memory.

If the application restarts:

```text
notes = []
```

starts again.

The data is gone.

A database allows the application to store information beyond the lifetime of the running Python process.

---

# 🐘 16. What is PostgreSQL?

PostgreSQL is a relational database management system.

Instead of storing application data in Python variables, the backend can store it in database tables.

For example:

```text
notes
------------------------------------------------
id | title       | content          | category
------------------------------------------------
1  | FastAPI     | Learning routes  | Python
2  | Async       | Async notes      | Python
3  | PostgreSQL  | Database notes   | Database
```

The table contains rows and columns.

---

# 📊 17. Tables, Rows and Columns

Think of a table like structured data.

```text
users
------------------------------------
id | name       | email
------------------------------------
1  | Sarah      | sarah@example.com
2  | John       | john@example.com
```

### Table

```text
users
```

represents a type of data.

### Columns

```text
id
name
email
```

describe the fields.

### Row

```text
1 | Sarah | sarah@example.com
```

represents one record.

---

# 🔑 18. Primary Keys

Most tables have a unique identifier.

Example:

```text
id
```

For example:

```text
notes

id = 1
id = 2
id = 3
```

The primary key uniquely identifies each row.

That allows the backend to request:

```text
GET /notes/2
```

and find the database record with:

```text
id = 2
```

---

# 🔗 19. Foreign Keys

Foreign keys connect tables.

Imagine:

```text
users
----------------
id
name
email
```

and:

```text
notes
----------------
id
user_id
title
content
```

`user_id` can point to:

```text
users.id
```

Conceptually:

```text
User
  │
  ├── Note 1
  ├── Note 2
  └── Note 3
```

This becomes extremely important when building larger applications.

---

# 🧠 20. Relational Databases

PostgreSQL is called relational because tables can have relationships.

For example:

```text
Business
   │
   ├── Users
   │
   ├── Leads
   │
   └── Calls
```

The relationships are represented using keys.

This is useful for SaaS and AI applications where data belongs to different users, organisations or resources.

---

# 💬 21. SQL

SQL stands for Structured Query Language.

It is used to communicate with relational databases.

Create:

```sql
INSERT INTO notes (title, content)
VALUES ('FastAPI', 'Learning FastAPI');
```

Read:

```sql
SELECT * FROM notes;
```

Update:

```sql
UPDATE notes
SET title = 'FastAPI Updated'
WHERE id = 1;
```

Delete:

```sql
DELETE FROM notes
WHERE id = 1;
```

These operations are the database equivalent of CRUD.

---

# 🔄 22. API CRUD vs Database CRUD

This connection is important.

```text
HTTP              Database

POST /notes   →   INSERT

GET /notes    →   SELECT

PUT /notes/1  →   UPDATE

DELETE /notes/1
               →  DELETE
```

The API receives the HTTP request.

The backend translates the request into application/database operations.

---

# 🧱 23. What is an ORM?

ORM means:

**Object Relational Mapper**

An ORM lets developers work with database tables using programming-language objects instead of writing raw SQL for every operation.

A common Python ORM is SQLAlchemy.

Conceptually:

```text
Python Object
      ↕
SQLAlchemy
      ↕
SQL
      ↕
PostgreSQL
```

Instead of thinking only in SQL:

```sql
SELECT * FROM notes;
```

the application can work with Python models and queries.

Learning SQL is still valuable because the ORM ultimately interacts with the relational database.

---

# 🔗 24. SQLAlchemy

SQLAlchemy is commonly used in Python backend applications to communicate with relational databases.

A model might conceptually represent:

```python
class Note:
    id
    title
    content
    category
```

which maps to:

```text
notes table

id
title
content
category
```

The important idea is:

```text
Python
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

SQLAlchemy does not replace PostgreSQL.

PostgreSQL is the database.

SQLAlchemy helps the Python application communicate with it.

---

# 🔌 25. Database Connection

FastAPI needs a way to communicate with PostgreSQL.

Conceptually:

```text
FastAPI
   ↓
Database Session / Connection
   ↓
SQLAlchemy
   ↓
PostgreSQL
```

A database URL may look conceptually like:

```text
postgresql://username:password@host:5432/database_name
```

Credentials should not be hardcoded into source code.

Instead, configuration can come from environment variables.

Example:

```text
DATABASE_URL=...
```

The real `.env` file should not be committed to Git.

---

# 💉 26. FastAPI Dependencies

FastAPI has a dependency injection system.

A dependency is functionality that a route needs but does not need to create itself every time.

For example:

```text
GET /notes
     ↓
Needs database session
     ↓
Dependency provides session
     ↓
Route uses session
```

Conceptually:

```python
def get_db():
    ...
```

Then a route can depend on it.

Dependencies are commonly useful for:

- Database sessions
- Authentication
- Current users
- Permissions
- Configuration
- Shared services

---

# 🧠 27. Why Dependencies Matter

Without reusable dependencies, many routes could repeat the same setup code.

For example:

```text
Route 1 → Create DB connection
Route 2 → Create DB connection
Route 3 → Create DB connection
Route 4 → Create DB connection
```

Instead:

```text
              get_db()
                 │
        ┌────────┼────────┐
        ↓        ↓        ↓
     Route 1  Route 2  Route 3
```

The shared logic is managed in one place.

---

# 🔄 28. Database Migrations

Database structures change as applications evolve.

Version 1:

```text
notes

id
title
content
```

Later I decide I need:

```text
category
```

The new structure becomes:

```text
notes

id
title
content
category
```

Simply changing Python code does not always safely update an existing production database.

That is why migrations exist.

---

# 🛠️ 29. Alembic

Alembic is a database migration tool commonly used with SQLAlchemy.

It tracks changes to the database schema.

Conceptually:

```text
Database Version 1

notes
- id
- title
- content

        ↓ migration

Database Version 2

notes
- id
- title
- content
- category
```

Migrations make schema changes:

- Repeatable
- Trackable
- Reversible in many cases
- Easier to deploy consistently

For Week 4, I mainly want to understand WHY migrations exist.

---

# 🚨 30. HTTP Status Codes

An API should communicate what happened.

Common status codes:

```text
200 OK
Request succeeded.

201 Created
A new resource was created.

204 No Content
Request succeeded but there is no response body.

400 Bad Request
The request is invalid.

401 Unauthorized
Authentication is required or invalid.

403 Forbidden
The user is authenticated but not allowed to perform the action.

404 Not Found
The requested resource does not exist.

422 Unprocessable Content
The request structure/data failed validation.

500 Internal Server Error
Something failed on the server.
```

Status codes are part of the contract between the client and backend.

---

# ❌ 31. Error Handling

Imagine requesting:

```text
GET /notes/999
```

but note `999` does not exist.

The backend should not simply crash.

FastAPI can return an HTTP error.

Example:

```python
from fastapi import HTTPException


raise HTTPException(
    status_code=404,
    detail="Note not found"
)
```

The client receives something like:

```json
{
  "detail": "Note not found"
}
```

---

# 📚 32. Automatic API Documentation

One useful FastAPI feature is automatically generated API documentation.

When the development server is running, FastAPI commonly exposes interactive documentation at:

```text
/docs
```

This lets me inspect and test endpoints from the browser.

I can test:

```text
GET
POST
PUT
DELETE
```

without first building a frontend.

There is also alternative documentation commonly available at:

```text
/redoc
```

---

# 🧪 33. Testing APIs

A backend working once does not mean it is reliable.

I should test successful and unsuccessful situations.

For example:

```text
Create valid note
        ↓
201 Created

Retrieve note
        ↓
200 OK

Retrieve unknown note
        ↓
404 Not Found

Create invalid note
        ↓
Validation error

Update note
        ↓
Successful update

Delete note
        ↓
Successful deletion
```

Testing helps verify the behaviour of the API.

---

# ⚡ 34. Async FastAPI

From Week 3 I learned:

```python
async def
```

and:

```python
await
```

FastAPI also supports asynchronous route functions.

Example:

```python
@app.get("/notes")
async def get_notes():
    ...
```

This becomes useful when a route performs asynchronous I/O such as:

```text
Database operations

External API requests

LLM requests

Agent tool calls

Network operations
```

The important lesson from Week 3 still applies:

> Async does not magically make everything faster.

It helps the application use waiting time efficiently for suitable I/O operations.

---

# 🏗️ 35. Full Backend Request Flow

This is the main architecture I want to understand this week.

```text
Client
  │
  │ POST /notes
  ↓
FastAPI Router
  │
  ↓
Pydantic Validation
  │
  ↓
Application Logic
  │
  ↓
Database Dependency
  │
  ↓
SQLAlchemy
  │
  ↓
PostgreSQL
  │
  ↓
Database Result
  │
  ↓
Response Model
  │
  ↓
JSON Response
  │
  ↓
Client
```

Each part has a responsibility.

### FastAPI

Handles the web/API layer.

### Pydantic

Validates and structures data.

### SQLAlchemy

Helps Python communicate with the relational database.

### PostgreSQL

Stores the application's persistent data.

### Alembic

Tracks changes to the database schema.

---

# 🛠️ 36. Week 4 Project

## Developer Notes / Knowledge API

The project for this week is a simple Developer Notes API.

The purpose is not to build a large product.

The purpose is to connect all the concepts together.

A developer can store notes such as:

```json
{
  "title": "Understanding async",
  "content": "Async helps Python use waiting time efficiently.",
  "category": "Python"
}
```

Possible database structure:

```text
notes
---------------------------------
id
title
content
category
created_at
updated_at
```

---

# 🛣️ 37. Developer Notes Endpoints

```text
GET /notes
```

Return all notes.

```text
GET /notes/{id}
```

Return one note.

```text
POST /notes
```

Create a note.

```text
PUT /notes/{id}
```

Update a note.

```text
DELETE /notes/{id}
```

Delete a note.

This gives me a complete CRUD API.

---

# 🧩 38. Project Architecture

A small version might begin as:

```text
developer-notes-api/
│
├── main.py
├── database.py
├── models.py
├── schemas.py
└── requirements.txt
```

Responsibilities:

```text
main.py
→ FastAPI application and routes

database.py
→ Database connection

models.py
→ Database models

schemas.py
→ Pydantic request/response schemas
```

As applications become larger, this structure can be separated further into routers, services, repositories and other layers.

For Week 4, I want to understand the responsibilities before worrying about complex architecture.

---

# 🔍 39. Models vs Schemas

This is an important distinction.

A database model represents how data is stored.

Example:

```text
Database Model

Note
├── id
├── title
├── content
├── category
└── created_at
```

A Pydantic schema represents data entering or leaving the API.

For example:

```text
NoteCreate

title
content
category
```

Notice that the client does not necessarily provide:

```text
id
created_at
```

The server/database can generate those.

So:

```text
Pydantic Schema
      ↓
What API data should look like

Database Model
      ↓
How data is stored
```

They serve different responsibilities even when some fields are similar.

---

# 🔐 40. Environment Variables

Sensitive configuration should not be hardcoded.

Bad:

```python
password = "my-real-database-password"
```

Better conceptually:

```text
.env

DATABASE_URL=...
```

Then:

```text
.gitignore

.env
```

The repository can contain:

```text
.env.example
```

with placeholders instead of real credentials.

---

# 🤖 41. Why This Matters for AI Engineering

AI systems still need normal backend engineering.

An AI Agent application might look like:

```text
Frontend
   ↓
FastAPI
   ↓
Agent
   ├── LLM
   ├── Tools
   ├── External APIs
   └── Retrieval
   ↓
PostgreSQL
```

The AI model is only one component of the system.

The backend still needs to handle:

- Requests
- Authentication
- Validation
- Users
- Agent state
- Conversations
- Tool results
- Database records
- Errors
- Logging
- Security

Understanding backend fundamentals makes it easier to understand the entire AI system.

---

# 🔗 42. Connecting Weeks 1-4

## Week 1 - Python Foundations

I learned the language fundamentals:

```text
Variables
Lists
Dictionaries
Loops
Functions
Files
JSON
```

↓

## Week 2 - OOP

I learned how code can be structured around objects and responsibilities:

```text
Classes
Objects
Methods
State
Inheritance
Composition
```

↓

## Week 3 - Async Python & APIs

I learned how Python communicates with external systems:

```text
HTTP
APIs
async
await
httpx
Concurrency
Timeouts
Failure handling
```

↓

## Week 4 - FastAPI & PostgreSQL

Now those concepts start becoming a backend:

```text
Python
   +
Async
   +
HTTP
   +
FastAPI
   +
Pydantic
   +
PostgreSQL
   ↓
Backend Service
```

---

# 💡 43. Key Mental Model

The biggest concept I want to remember from Week 4 is:

```text
REQUEST
   ↓
ROUTE
   ↓
VALIDATE
   ↓
PROCESS
   ↓
DATABASE
   ↓
RESPONSE
```

If I understand what happens at each step, I understand the foundation of a backend API.

---

# 🎯 44. What I Should Be Able to Explain After Week 4

By the end of Week 4, I should be able to explain in my own words:

**FastAPI**

How Python functions become API endpoints.

**HTTP**

How clients communicate with backend services.

**Routing**

How FastAPI decides which Python function handles a request.

**Pydantic**

How incoming and outgoing data is structured and validated.

**CRUD**

How applications create, read, update and delete data.

**PostgreSQL**

Where persistent relational data is stored.

**SQLAlchemy**

How Python can work with a relational database through an ORM/toolkit.

**Dependencies**

How reusable functionality such as database sessions can be provided to routes.

**Migrations**

How database schemas change safely as an application evolves.

**Testing**

How I verify both successful behaviour and failure cases.

---

# 🎥 45. Weekly Wrap-Up

For my Week 4 wrap-up, I want to demonstrate:

### 1. Start the FastAPI backend

```text
Python → FastAPI server
```

### 2. Open the API documentation

```text
/docs
```

### 3. Create a developer note

```text
POST /notes
```

### 4. Retrieve the note

```text
GET /notes
```

### 5. Show the stored PostgreSQL data

```text
FastAPI → PostgreSQL
```

### 6. Update the note

```text
PUT /notes/{id}
```

### 7. Delete the note

```text
DELETE /notes/{id}
```

### 8. Trigger an error

For example:

```text
GET /notes/999
```

and demonstrate:

```text
404 Not Found
```

The goal of the demonstration is to show:

> How Python becomes a real backend service.

---

# 🧠 My Week 4 Summary

Before this week, I understood Python mainly as the language running my application logic.

FastAPI shows how that Python logic can be exposed through HTTP endpoints.

Pydantic provides a validation layer around the data entering and leaving the application.

PostgreSQL provides persistent storage.

SQLAlchemy connects the Python application to the relational database.

Alembic provides a way to evolve the database structure as the application changes.

Together:

```text
FastAPI
   +
Pydantic
   +
SQLAlchemy
   +
PostgreSQL
   +
Alembic
   ↓
Production-style Python Backend Foundation
```

This same foundation can later sit underneath LLM applications and AI Agents.

---

# 🔄 Learning Process

My approach throughout this challenge:

**Learn → Attempt → Break → Debug → Understand → Build → Document**

The goal is not just to make the code work.

The goal is to understand **why it works, what each component is responsible for, and what happens when it fails.**

---

