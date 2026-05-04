import { useState, useEffect } from 'react';
import { getTodos, createTodo } from './api.js';
import TodoItem from './TodoItem.jsx';

const FILTERS = ['all', 'pending', 'completed'];

export default function TodoList() {
  const [todos, setTodos] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [filter, setFilter] = useState('all');

  async function fetchTodos(status = filter) {
    const data = await getTodos(status);
    setTodos(data);
  }

  useEffect(() => {
    fetchTodos(filter);
  }, [filter]);

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
      <div className="filter-tabs">
        {FILTERS.map((f) => (
          <button
            key={f}
            className={`btn-filter${filter === f ? ' active' : ''}`}
            onClick={() => setFilter(f)}
          >
            {f.charAt(0).toUpperCase() + f.slice(1)}
          </button>
        ))}
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
