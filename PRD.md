# MyTodos — Product Requirements Document

**Version:** 1.0
**Owner:** Product
**Status:** Draft

---

## 1. Overview

MyTodos is a simple, single-user web application for managing a personal to-do list. The product enables a user to capture tasks, mark them complete when done, and remove them when no longer needed. The goal is to ship a clean, minimal experience with no friction — open the app, add a task, get on with the day.

This document describes the scope for **v1.0**.

---

## 2. Goals & Non-Goals

### Goals

- Provide a fast, distraction-free way to manage a personal task list.
- Demonstrate a working full-stack architecture using React (Vite) and FastAPI.
- Ship a usable product with the smallest possible feature set.

### Non-Goals (out of scope for v1)

- User accounts, authentication, or multi-user support.
- Persistent storage in a database (in-memory store is acceptable for v1).
- Categories, tags, due dates, reminders, priorities, or attachments.
- Mobile native apps. (The web app should be responsive, but no native build.)
- Sharing, collaboration, or sync across devices.

---

## 3. Target User

A single user who wants a lightweight personal task list on the web. No persona segmentation in v1.

---

## 4. User Stories

1. As a user, I want to **add a new todo** by typing a short description so I can capture a task quickly.
2. As a user, I want to **see all my todos** in a single list so I know what's outstanding.
3. As a user, I want to **mark a todo as complete** so I can track what I've finished.
4. As a user, I want to **unmark a completed todo** in case I checked it off by mistake.
5. As a user, I want to **delete a todo** so I can remove tasks I no longer need.

---

## 5. Functional Requirements

### 5.1 Create Todo

- Input field accepts plain text, 1–200 characters.
- Empty or whitespace-only entries are rejected (no error toast needed; the Add button is simply disabled).
- New todos appear at the top of the list and default to **incomplete**.

### 5.2 View Todos

- All todos are displayed in a single list, newest first.
- Each item shows: the todo text, a checkbox indicating completion, and a delete button.
- Completed items are visually distinguished (e.g., strikethrough, muted color).

### 5.3 Mark Complete / Incomplete

- Clicking the checkbox toggles the completion state.
- The change is reflected in the UI immediately and persisted on the backend.

### 5.4 Delete Todo

- Clicking the delete button removes the todo from the list.
- No confirmation dialog in v1 (keeping it simple).

---

## 6. Non-Functional Requirements

- **Performance:** UI actions should feel instant. API responses should return in under 200 ms on localhost.
- **Reliability:** All API errors should be handled gracefully; the UI should not crash on a failed request.
- **Usability:** The interface should be readable on screens 320 px wide and up.
- **Compatibility:** Latest two versions of Chrome, Firefox, Safari, and Edge.

---

## 7. Technical Architecture

### 7.1 Stack

| Layer         | Technology                                 |
| ------------- | ------------------------------------------ |
| Frontend      | React (with Vite), plain CSS               |
| Backend       | Python with FastAPI                        |
| Storage       | In-memory list (no database for v1)        |
| Communication | REST over JSON, CORS enabled for local dev |

### 7.2 API Endpoints

| Method | Endpoint      | Purpose                                                       |
| ------ | ------------- | ------------------------------------------------------------- |
| GET    | `/todos`      | Return the full list of todos                                 |
| POST   | `/todos`      | Create a new todo. Body: `{ "text": string }`                 |
| PATCH  | `/todos/{id}` | Toggle or update completion. Body: `{ "completed": boolean }` |
| DELETE | `/todos/{id}` | Delete a todo by id                                           |

### 7.3 Data Model

```json
{
  "id": "string (uuid)",
  "text": "string",
  "completed": false,
  "created_at": "ISO 8601 timestamp"
}
```

### 7.4 Project Structure

```
mytodos/
├── backend/
│   ├── main.py           # FastAPI app, routes, in-memory store
│   └── requirements.txt
└── frontend/
    ├── src/
    │   ├── App.jsx       # Main component
    │   ├── api.js        # Fetch helpers
    │   └── main.jsx
    ├── index.html
    └── package.json
```

---

## 8. UI Layout

A single screen with:

1. **Header** — App title "MyTodos".
2. **Input row** — Text field + "Add" button.
3. **List** — Todo items, each with a checkbox, the text, and a delete (×) button.
4. **Empty state** — A short message when the list is empty (e.g., "Nothing here yet. Add your first todo above.").

---

## 9. Success Criteria

- A user can add, complete, uncomplete, and delete todos without any errors.
- The frontend and backend run locally with two commands (`npm run dev` and `uvicorn main:app --reload`).
- The full round-trip for any action takes under 200 ms on localhost.

---

## 10. Future Considerations (post-v1)

- Persistent storage (SQLite or Postgres).
- User accounts and authentication.
- Due dates, priorities, and categories.
- Search and filter.
- Deployment to a hosted environment.
