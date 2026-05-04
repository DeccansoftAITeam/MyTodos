from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Literal, Optional

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

todos: list[dict] = []
next_id: int = 1


class TodoCreate(BaseModel):
    title: str


class TodoUpdate(BaseModel):
    title: Optional[str] = None
    completed: Optional[bool] = None


@app.get("/health")
def health_check() -> dict:
    return {"status": "ok"}


@app.get("/todos")
def get_todos(status: Literal["all", "pending", "completed"] = "all") -> list[dict]:
    if status == "completed":
        return [t for t in todos if t["completed"]]
    if status == "pending":
        return [t for t in todos if not t["completed"]]
    return todos


@app.post("/todos", status_code=201)
def create_todo(body: TodoCreate) -> dict:
    global next_id
    todo = {"id": next_id, "title": body.title, "completed": False}
    todos.append(todo)
    next_id += 1
    return todo


@app.put("/todos/{todo_id}")
def update_todo(todo_id: int, body: TodoUpdate) -> dict:
    for todo in todos:
        if todo["id"] == todo_id:
            if body.title is not None:
                todo["title"] = body.title
            if body.completed is not None:
                todo["completed"] = body.completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}", status_code=204)
def delete_todo(todo_id: int) -> None:
    for i, todo in enumerate(todos):
        if todo["id"] == todo_id:
            todos.pop(i)
            return
    raise HTTPException(status_code=404, detail="Todo not found")
