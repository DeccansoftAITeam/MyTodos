import pytest
import main
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_state():
    main.todos.clear()
    main.next_id = 1
    yield


# --- GET /health ---

def test_health_returns_200():
    r = client.get("/health")
    assert r.status_code == 200


def test_health_returns_ok_body():
    r = client.get("/health")
    assert r.json() == {"status": "ok"}


# --- GET /todos ---

def test_get_todos_empty():
    r = client.get("/todos")
    assert r.status_code == 200
    assert r.json() == []


def test_get_todos_returns_all():
    client.post("/todos", json={"title": "First"})
    client.post("/todos", json={"title": "Second"})
    r = client.get("/todos")
    assert len(r.json()) == 2


def test_get_todos_shape():
    client.post("/todos", json={"title": "Check shape"})
    item = client.get("/todos").json()[0]
    assert "id" in item
    assert "title" in item
    assert "completed" in item


def test_get_todos_completed_default_false():
    client.post("/todos", json={"title": "New"})
    item = client.get("/todos").json()[0]
    assert item["completed"] is False


# --- POST /todos ---

def test_create_todo_returns_201():
    r = client.post("/todos", json={"title": "Buy milk"})
    assert r.status_code == 201


def test_create_todo_returns_correct_shape():
    r = client.post("/todos", json={"title": "Buy milk"})
    body = r.json()
    assert "id" in body
    assert "title" in body
    assert "completed" in body


def test_create_todo_title_is_preserved():
    r = client.post("/todos", json={"title": "Buy milk"})
    assert r.json()["title"] == "Buy milk"


def test_create_todo_completed_is_false():
    r = client.post("/todos", json={"title": "Buy milk"})
    assert r.json()["completed"] is False


def test_create_todo_id_increments():
    r1 = client.post("/todos", json={"title": "First"})
    r2 = client.post("/todos", json={"title": "Second"})
    assert r2.json()["id"] == r1.json()["id"] + 1


def test_create_todo_missing_title_returns_422():
    r = client.post("/todos", json={})
    assert r.status_code == 422


# --- PUT /todos/{todo_id} ---

def test_update_todo_returns_200():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": "Updated"})
    assert r.status_code == 200


def test_update_title_only():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": "Changed"})
    body = r.json()
    assert body["title"] == "Changed"
    assert body["completed"] is False


def test_update_completed_only():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"completed": True})
    body = r.json()
    assert body["completed"] is True
    assert body["title"] == "Original"


def test_update_both_fields():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={"title": "New", "completed": True})
    body = r.json()
    assert body["title"] == "New"
    assert body["completed"] is True


def test_update_empty_body_no_change():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    r = client.put(f"/todos/{todo_id}", json={})
    body = r.json()
    assert body["title"] == "Original"
    assert body["completed"] is False


def test_update_nonexistent_id_returns_404():
    r = client.put("/todos/9999", json={"title": "Ghost"})
    assert r.status_code == 404


def test_update_returns_updated_todo_on_get():
    todo_id = client.post("/todos", json={"title": "Original"}).json()["id"]
    client.put(f"/todos/{todo_id}", json={"title": "Updated", "completed": True})
    items = client.get("/todos").json()
    assert items[0]["title"] == "Updated"
    assert items[0]["completed"] is True


# --- DELETE /todos/{todo_id} ---

def test_delete_todo_returns_204():
    todo_id = client.post("/todos", json={"title": "To delete"}).json()["id"]
    r = client.delete(f"/todos/{todo_id}")
    assert r.status_code == 204


def test_delete_response_body_is_empty():
    todo_id = client.post("/todos", json={"title": "To delete"}).json()["id"]
    r = client.delete(f"/todos/{todo_id}")
    assert r.content == b""


def test_delete_removes_from_list():
    todo_id = client.post("/todos", json={"title": "To delete"}).json()["id"]
    client.delete(f"/todos/{todo_id}")
    assert client.get("/todos").json() == []


def test_delete_nonexistent_id_returns_404():
    r = client.delete("/todos/9999")
    assert r.status_code == 404


def test_delete_only_removes_target():
    id1 = client.post("/todos", json={"title": "Keep"}).json()["id"]
    id2 = client.post("/todos", json={"title": "Remove"}).json()["id"]
    client.delete(f"/todos/{id2}")
    items = client.get("/todos").json()
    assert len(items) == 1
    assert items[0]["id"] == id1
