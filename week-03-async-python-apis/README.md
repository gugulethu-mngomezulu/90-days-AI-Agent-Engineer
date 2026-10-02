# ⚡ Week 03 - Async Python & APIs

## 90 Days of AI Agent Engineering

### Level: Developing

Week 3 of my **90 Days of AI Agent Engineering** challenge focuses on understanding how Python applications communicate with external systems and how asynchronous programming can make I/O-heavy applications more efficient.

As an AI Engineer working with agentic systems, APIs are an important part of the systems I build. This week is about going back to the fundamentals and making sure I understand what is happening underneath the frameworks and tools I use.

---

## 🎯 Week 3 Goals

This week I'm learning:

- HTTP fundamentals
- REST APIs
- HTTP methods and status codes
- JSON responses
- Python `requests`
- `httpx`
- `async` and `await`
- `asyncio`
- Concurrent API requests
- Timeouts
- Retries
- Exception handling
- Environment variables
- API failure handling

---

## 🧠 What I Want to Understand

By the end of this week, I want to be able to explain:

> What happens when a Python application sends a request to an API?

I also want to understand the difference between synchronous and asynchronous code.

Instead of simply knowing where to write `async` and `await`, I want to understand **why and when they are useful**.

---

## 🛠️ Week 3 Project

### Async API Collector

I will build a Python application that collects data from multiple APIs.

The project will start with normal synchronous API requests and then be improved using asynchronous Python.

The goal is to compare the two approaches and understand how concurrency can improve applications that spend time waiting for external services.

---

## 🏗️ Project Flow

```text
Python Application
        |
        |---- API Request 1
        |
        |---- API Request 2
        |
        |---- API Request 3
        |
        ↓
Collect Results
        ↓
Display Data

### Synchronous
With synchronous code, the application waits for one request to finish before starting the next request.

Request 1 → Wait → Response
                     ↓
Request 2 → Wait → Response
                     ↓
Request 3 → Wait → Response

### Asynchronous
With asynchronous code, the program can work on another request while waiting for a previous request to return.

Request 1 ─────────→
Request 2 ─────────→
Request 3 ─────────→

        ↓

Collect Responses

This is especially useful when working with:
- APIs
- Databases
- AI models
- Agent tools
- Network services

### 🧪 Failure Handling

A successful API request is only part of the project.
I will intentionally test failures such as:
- Invalid URLs
- API timeouts
- 404 responses
- 429 rate limits
- 500 server errors
- Connection errors

The application should handle these failures without crashing unexpectedly.

### 🔐 Environment Variables

API keys and secrets should not be stored directly inside the source code.
I will practice using environment variables and make sure sensitive files such as .env are excluded from Git.

### 💡 Key Question
One of the main questions I want to answer this week is:
Why is asynchronous programming useful when building AI agents?

AI systems often spend time waiting for external operations such as LLM responses, APIs, databases and tools.
Understanding asynchronous Python will help me understand how these systems can handle that waiting time more efficiently.