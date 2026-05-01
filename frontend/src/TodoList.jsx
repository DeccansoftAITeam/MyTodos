import { useState, useEffect } from 'react';
import { getTodos, createTodo } from './api.js';
import TodoItem from './TodoItem.jsx';

export default function TodoList() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');

  async function fetchTodos() {
    const data = await getTodos();
    setTodos(data);
  }

  useEffect(() => {
    fetchTodos();
  }, []);

  async function handleAdd() {
    const title = inputValue.trim();
    if (!title) return;
    await createTodo(title);
    setInputValue('');
    fetchTodos();
  }

  function handleKeyDown(e) {
    if (e.key === 'Enter') handleAdd();
  }

  return (
    <div className="todo-container">
      <h1>My Todos</h1>
      <div className="todo-input-row">
        <input
          type="text"
          placeholder="Add a new todo..."
          value={inputValue}
          onChange={(e) => setInputValue(e.target.value)}
          onKeyDown={handleKeyDown}
        />
        <button className="btn-add" onClick={handleAdd}>Add</button>
      </div>
      {todos.length === 0 ? (
        <p className="empty-message">No todos yet. Add one above!</p>
      ) : (
        <ul className="todo-list">
          {todos.map((todo) => (
            <TodoItem key={todo.id} todo={todo} onRefresh={fetchTodos} />
          ))}
        </ul>
      )}
    </div>
  );
}
