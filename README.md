# FastAPI To-Do List CRUD API 🚀

A lightweight, lightning-fast RESTful API for managing a To-Do list, built with [FastAPI](https://fastapi.tiangolo.com/) and Python. 

This project demonstrates a complete CRUD (Create, Read, Update, Delete) implementation using an in-memory database and Pydantic models for strict data validation.

---

## ✨ Features

- **Fast & Modern**: Built with FastAPI, one of the fastest Python frameworks available.
- **Data Validation**: Automatic request and response validation using Pydantic.
- **Interactive Documentation**: Auto-generated Swagger UI and ReDoc documentation.
- **In-Memory Storage**: Uses a simple Python list to store tasks temporarily.

---

## 🛠️ Getting Started

Follow these instructions to get a copy of the project up and running on your local machine.

### Prerequisites

You need Python 3.7+ installed. It is highly recommended to use a virtual environment.

### Installation & Setup

1. **Clone the repository** (if you haven't already):
   ```bash
   git clone https://github.com/shamilhossain/crud-api.git
   cd "crud api"
   ```

2. **Activate your virtual environment**:
   ```bash
   source .venv/bin/activate
   ```

3. **Install dependencies** (FastAPI and Uvicorn):
   ```bash
   pip install fastapi uvicorn
   ```

4. **Run the API server**:
   ```bash
   uvicorn main:app --reload
   ```

The server will start at `http://127.0.0.1:8000`. The `--reload` flag ensures the server automatically restarts when you save code changes.

---

## 📖 API Reference

Here are the available endpoints. All data is sent and received in JSON format.

| Method | Endpoint | Description | Status Codes |
|---|---|---|---|
| **GET** | `/` | Returns API metadata & version | 200 OK |
| **GET** | `/health` | Returns API health status | 200 OK |
| **GET** | `/tasks` | Retrieves all tasks | 200 OK |
| **GET** | `/tasks/{id}` | Retrieves a specific task by ID | 200 OK, 404 Not Found |
| **POST** | `/tasks` | Creates a new task | 201 Created, 400 Bad Request |
| **PUT** | `/tasks/{id}` | Updates an existing task | 200 OK, 400 Bad Request, 404 Not Found |
| **DELETE**| `/tasks/{id}` | Deletes a task by ID | 204 No Content, 404 Not Found |

### Example Request (POST)

To create a new task via `curl` from your terminal:

```bash
curl -X POST http://127.0.0.1:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Learn FastAPI", "done": false}'
```

**Response:**
```json
{
  "id": 4,
  "title": "Learn FastAPI",
  "done": false
}
```

---

## 🔍 Interactive Documentation

FastAPI automatically generates beautiful, interactive API documentation. While the server is running, you can visit:

- **[Swagger UI](http://127.0.0.1:8000/docs)**: Allows you to explore the API and test endpoints directly from your browser by clicking **"Try it out"**.
- **[ReDoc](http://127.0.0.1:8000/redoc)**: An alternative, highly readable documentation layout.

*(You can add a screenshot of your Swagger UI here by replacing the placeholder image name)*
![Swagger UI](placeholder_for_swagger_screenshot.png)

---

## 🧪 Mortality Experiment

Because we use an in-memory Python list (`tasks_db`) instead of a real database, all data is temporarily stored in the server's RAM. Whenever the server restarts or crashes, this memory is cleared, causing any newly created or updated tasks to be lost and reset to the hardcoded defaults.

---

## 🤖 Stage 7: AI Rematch (AI vs Me)

### The Prompt
I asked an AI to generate the API with this prompt:
> "Write a FastAPI To-Do List CRUD API. Use an in-memory list with 3 dummy tasks. The model should have id, title, and done. Create GET all, GET by id, POST, PUT, and DELETE endpoints. Use Pydantic for validation."

### What the AI did better
The AI utilized Pydantic's `Field` function which makes the models cleaner and allows for built-in metadata like descriptions. It also used `**task.dict()` to unpack the model cleanly, saving a few lines of code during task creation and updates.

### What the AI got wrong / ignored
The AI completely missed the `201 Created` status code on the `POST` endpoint, returning the default `200 OK` instead. It also did not implement any custom validation to prevent empty strings for titles, allowing users to submit blanks.

### What my prompt forgot to specify
I realized I forgot to explicitly tell the AI to return a `404` for missing IDs in the PUT and DELETE endpoints (though it guessed it right anyway), and I didn't specify that I wanted to manually block empty or whitespace-only strings for titles!
