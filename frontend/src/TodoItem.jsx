import { updateTodo, deleteTodo } from './api.js';

export default function TodoItem({ todo, onRefresh }) {
  async function handleToggle() {
    await updateTodo(todo.id, { completed: !todo.completed });
    onRefresh();
  }

  async function handleDelete() {
    await deleteTodo(todo.id);
    onRefresh();
  }

  return (
    <li className={`todo-item${todo.completed ? ' completed' : ''}`}>
      <input
        type="checkbox"
        checked={todo.completed}
        onChange={handleToggle}
      />
      <span className="todo-title">{todo.title}</span>
      <button className="btn-delete" onClick={handleDelete}>Delete</button>
    </li>
  );
}
