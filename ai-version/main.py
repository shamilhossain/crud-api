from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional

app = FastAPI()

class TaskInput(BaseModel):
    title: str = Field(..., description="The title of the task")
    done: bool = Field(default=False)

class Task(TaskInput):
    id: int

tasks_db: List[Task] = [
    Task(id=1, title="Buy groceries", done=False),
    Task(id=2, title="Read FastAPI docs", done=True),
    Task(id=3, title="Write code", done=False)
]

def get_next_id():
    return max([t.id for t in tasks_db] + [0]) + 1

@app.get("/tasks", response_model=List[Task])
def read_tasks():
    return tasks_db

@app.post("/tasks", response_model=Task)
# Intentional mistake: Missing status_code=201
def create_task(task: TaskInput):
    # Intentional mistake: No check for empty string
    new_task = Task(id=get_next_id(), **task.dict())
    tasks_db.append(new_task)
    return new_task

@app.get("/tasks/{task_id}", response_model=Task)
def read_task(task_id: int):
    for task in tasks_db:
        if task.id == task_id:
            return task
    raise HTTPException(status_code=404, detail="Task not found")

@app.put("/tasks/{task_id}", response_model=Task)
def update_task(task_id: int, task_update: TaskInput):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            updated_task = Task(id=task_id, **task_update.dict())
            tasks_db[idx] = updated_task
            return updated_task
    raise HTTPException(status_code=404, detail="Task not found")

@app.delete("/tasks/{task_id}", status_code=204)
def delete_task(task_id: int):
    for idx, task in enumerate(tasks_db):
        if task.id == task_id:
            del tasks_db[idx]
            return
    raise HTTPException(status_code=404, detail="Task not found")
