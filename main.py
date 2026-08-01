from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class TaskInput(BaseModel):
    title: Optional[str] = None
    done: bool = False

class Task(BaseModel):
    id: int
    title: str
    done: bool

# In-memory database pre-filled with 3 sample tasks
tasks_db: List[Task] = [
    Task(id=1, title="Buy groceries", done=False),
    Task(id=2, title="Read FastAPI docs", done=True),
    Task(id=3, title="Write code", done=False)
]

def get_next_id() -> int:
    if not tasks_db:
        return 1
    return max(task.id for task in tasks_db) + 1

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/tasks", response_model=List[Task])
def get_tasks():
    return tasks_db

@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    for task in tasks_db:
        if task.id == id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task_in: TaskInput):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title is missing or empty")
    new_task = Task(id=get_next_id(), title=task_in.title.strip(), done=task_in.done)
    tasks_db.append(new_task)
    return new_task

@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task_in: TaskInput):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title is missing or empty")
    for i, task in enumerate(tasks_db):
        if task.id == id:
            updated_task = Task(id=id, title=task_in.title.strip(), done=task_in.done)
            tasks_db[i] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    for i, task in enumerate(tasks_db):
        if task.id == id:
            del tasks_db[i]
            return
    raise HTTPException(status_code=404, detail="Task not found")
