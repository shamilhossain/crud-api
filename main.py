import sqlite3
from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel
from typing import List, Optional
from contextlib import asynccontextmanager

DATABASE = "tasks.db"

def get_db_connection():
    conn = sqlite3.connect(DATABASE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    # Stage 0: Create the table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done BOOLEAN NOT NULL DEFAULT 0
        )
    ''')
    
    # Check if empty and insert dummy tasks
    cursor.execute('SELECT COUNT(*) FROM tasks')
    if cursor.fetchone()[0] == 0:
        sample_tasks = [
            ("Buy groceries", False),
            ("Read FastAPI docs", True),
            ("Write code", False)
        ]
        cursor.executemany('INSERT INTO tasks (title, done) VALUES (?, ?)', sample_tasks)
    
    conn.commit()
    conn.close()

# Run init_db on application startup
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(lifespan=lifespan)

class TaskInput(BaseModel):
    title: Optional[str] = None
    done: bool = False

class Task(BaseModel):
    id: int
    title: str
    done: bool

@app.get("/")
def read_root():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}

@app.get("/health")
def health_check():
    return {"status": "ok"}

# Stage 1: Read all tasks (with filtering extras preserved)
@app.get("/tasks", response_model=List[Task])
def get_tasks(done: Optional[bool] = None, search: Optional[str] = None):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    query = "SELECT * FROM tasks WHERE 1=1"
    params = []
    
    if done is not None:
        query += " AND done = ?"
        params.append(1 if done else 0)
    
    if search is not None:
        query += " AND title LIKE ?"
        params.append(f"%{search}%")
        
    cursor.execute(query, params)
    rows = cursor.fetchall()
    conn.close()
    
    # Convert Row objects to dictionaries
    return [dict(row) for row in rows]

# Stage 1: Read single task
@app.get("/tasks/{id}", response_model=Task)
def get_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    row = cursor.fetchone()
    conn.close()
    
    if row is None:
        raise HTTPException(status_code=404, detail="Task not found")
    return dict(row)

# Stage 2: Create task
@app.post("/tasks", status_code=status.HTTP_201_CREATED, response_model=Task)
def create_task(task_in: TaskInput):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title is missing or empty")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO tasks (title, done) VALUES (?, ?)", 
        (task_in.title.strip(), 1 if task_in.done else 0)
    )
    conn.commit()
    new_id = cursor.lastrowid
    
    # Fetch the newly created task to return
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (new_id,))
    new_task = cursor.fetchone()
    conn.close()
    
    return dict(new_task)

# Stage 3: Update task
@app.put("/tasks/{id}", response_model=Task)
def update_task(id: int, task_in: TaskInput):
    if not task_in.title or not task_in.title.strip():
        raise HTTPException(status_code=400, detail="Title is missing or empty")
        
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute(
        "UPDATE tasks SET title = ?, done = ? WHERE id = ?",
        (task_in.title.strip(), 1 if task_in.done else 0, id)
    )
    conn.commit()
    
    # Fetch the updated task
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    updated_task = cursor.fetchone()
    conn.close()
    
    return dict(updated_task)

# Stage 3: Delete task
@app.delete("/tasks/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(id: int):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if exists
    cursor.execute("SELECT * FROM tasks WHERE id = ?", (id,))
    if cursor.fetchone() is None:
        conn.close()
        raise HTTPException(status_code=404, detail="Task not found")
        
    cursor.execute("DELETE FROM tasks WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return

# Extra: Stats
@app.get("/stats")
def get_stats():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM tasks")
    total = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE done = 1")
    done_count = cursor.fetchone()[0]
    
    conn.close()
    return {"total": total, "done": done_count, "open": total - done_count}

# Extra: Reset DB
@app.post("/reset")
def reset_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DROP TABLE IF EXISTS tasks")
    conn.commit()
    conn.close()
    
    init_db()
    return {"message": "Database reset to defaults"}
