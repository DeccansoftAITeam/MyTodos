# MyTodos

A simple, single-user web application for managing a personal to-do list. Built with React (Vite) for the frontend and FastAPI for the backend.

## Features

- Add new todos with a clean, distraction-free interface
- Mark todos as complete or incomplete
- Delete todos you no longer need
- Instant feedback on all actions

## Quick Start

### Backend

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

The API server will start at `http://localhost:8000`.

### Frontend

```bash
cd frontend
npm install
npm run dev
```

The frontend will be available at `http://localhost:5173`.

## Architecture

| Layer      | Technology    |
| ---------- | ------------- |
| Frontend   | React + Vite  |
| Backend    | FastAPI       |
| Storage    | In-memory     |
| Comm       | REST + JSON   |

## Project Structure

```
mytodos/
├── backend/
│   ├── main.py              # FastAPI app with routes
│   └── requirements.txt      # Python dependencies
└── frontend/
    ├── src/
    │   ├── App.jsx          # Main component
    │   ├── main.jsx         # React entry point
    │   └── index.css        # Base styles
    ├── index.html           # HTML template
    ├── vite.config.js       # Vite configuration
    └── package.json         # Node dependencies
```

## API Endpoints

- `GET /health` — Health check
- `GET /todos` — Fetch all todos
- `POST /todos` — Create a new todo
- `PATCH /todos/{id}` — Update todo completion status
- `DELETE /todos/{id}` — Delete a todo

## Next Steps

1. Implement the Todo API endpoints in `backend/main.py`
2. Build the UI components in `frontend/src/App.jsx`
3. Connect frontend and backend with fetch calls
