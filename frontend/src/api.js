const BASE_URL = 'http://localhost:8000';

export async function getTodos(status = "all") {
  const res = await fetch(`${BASE_URL}/todos?status=${status}`);
  return res.json();
}

export async function createTodo(title) {
  const res = await fetch(`${BASE_URL}/todos`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ title }),
  });
  return res.json();
}

export async function updateTodo(id, fields) {
  const res = await fetch(`${BASE_URL}/todos/${id}`, {
    method: 'PUT',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(fields),
  });
  return res.json();
}

export async function deleteTodo(id) {
  await fetch(`${BASE_URL}/todos/${id}`, { method: 'DELETE' });
}
