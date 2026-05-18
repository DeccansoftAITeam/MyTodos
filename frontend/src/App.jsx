import TodoList from './TodoList.jsx';
import DateTime from './DateTime.jsx';
import './App.css';

export default function App() {
  return (
    <div className="app">
      <DateTime />
      <TodoList />
    </div>
  );
}
