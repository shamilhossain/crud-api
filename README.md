# Task API

A simple To-Do List CRUD API built with FastAPI.

## Running the API

To run the API locally, use the following command:

```bash
uvicorn main:app --reload
```

## Endpoints

| Method | Endpoint      | Description                          |
| ------ | ------------- | ------------------------------------ |
| GET    | `/`           | Returns API metadata                 |
| GET    | `/health`     | Returns health status                |
| GET    | `/tasks`      | Returns all tasks                    |
| GET    | `/tasks/{id}` | Returns a single task                |
| POST   | `/tasks`      | Creates a new task                   |
| PUT    | `/tasks/{id}` | Updates an existing task             |
| DELETE | `/tasks/{id}` | Deletes a task                       |

## Example curl command

```bash
curl -X POST http://127.0.0.1:8000/tasks \
     -H "Content-Type: application/json" \
     -d '{"title": "Test Task", "done": false}'
```

**Output:**
```json
{"id":4,"title":"Test Task","done":false}
```

## Swagger UI

You can view and interact with the API documentation at `http://127.0.0.1:8000/docs`.

![Swagger UI](placeholder_for_swagger_screenshot.png)
