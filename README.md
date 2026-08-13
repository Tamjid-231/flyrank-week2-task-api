# Task API

This is my Week 2 assignment for the FlyRank Backend Track. I built a small to-do API with Python and FastAPI to understand how CRUD operations work in a backend application.

The API can create, read, update and delete tasks. It uses an in-memory Python list instead of a database, so tasks created while the server is running disappear after a restart. The three sample tasks are then loaded again.

## What I learned

While building this project, I learned how an HTTP method and a path work together as an endpoint. I also practised request-body validation, JSON responses, status codes, Swagger UI and Git commits.

One important lesson was that the server should not trust every request. A missing or empty title returns a clear `400` response, and an unknown task ID returns `404` instead of an empty successful response.

## Project structure

```text
app/
  __init__.py
  main.py
docs/
  swagger-ui.png
tests/
  test_api.py
.gitignore
README.md
requirements.txt
requirements-dev.txt
```

- `app/main.py` contains the FastAPI application, models, validation and routes.
- `tests/test_api.py` checks the CRUD cycle, errors and status codes.
- `docs/swagger-ui.png` is evidence of the running interactive documentation.

## How it works

The server starts with three example tasks stored in a Python list. Each task contains an integer `id`, a text `title` and a boolean `done` value.

- `GET` reads tasks.
- `POST` creates a task, assigns the next ID and sets `done` to `false`.
- `PUT` changes the title, the done status, or both.
- `DELETE` removes a task and returns an empty `204` response.

The application uses Pydantic models to validate request data. FastAPI also creates the OpenAPI description and Swagger UI automatically.

## Install and run

Python 3.10 or newer is required.

Create a virtual environment:

```powershell
python -m venv .venv
```

Install the packages and start the server in Windows PowerShell:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe -m uvicorn app.main:app --reload
```

The API runs at `http://127.0.0.1:8000`.

- Swagger UI: `http://127.0.0.1:8000/docs`
- Health check: `http://127.0.0.1:8000/health`
- Task list: `http://127.0.0.1:8000/tasks`

## Endpoints

| Method | Path | Purpose | Success status |
| --- | --- | --- | --- |
| GET | `/` | Show API information | 200 |
| GET | `/health` | Check that the server is running | 200 |
| GET | `/tasks` | List all tasks | 200 |
| GET | `/tasks/{task_id}` | Get one task | 200 |
| POST | `/tasks` | Create a task | 201 |
| PUT | `/tasks/{task_id}` | Update a task | 200 |
| DELETE | `/tasks/{task_id}` | Delete a task | 204 |

## Request examples

Create a task:

```json
{
  "title": "Buy milk"
}
```

Update a task:

```json
{
  "title": "Buy milk today",
  "done": true
}
```

## Validation and errors

| Situation | Status | Response |
| --- | --- | --- |
| Missing or empty POST title | 400 | JSON error |
| Empty or invalid PUT body | 400 | JSON error |
| Unknown task ID | 404 | `{"error":"Task 99 not found"}` |
| Successful delete | 204 | Empty body |

## Example curl output

Command:

```bash
curl -i -X POST http://127.0.0.1:8000/tasks -H "Content-Type: application/json" -d '{"title":"Buy milk"}'
```

Output from the running API:

```text
HTTP/1.1 201 Created
server: uvicorn
content-type: application/json

{"id":4,"title":"Buy milk","done":false}
```

## Swagger UI

I tested the full CRUD cycle from Swagger UI: create a task, read it, update it, delete it and confirm that the deleted ID returns `404`.

![Task API Swagger UI](docs/swagger-ui.png)

## Run the tests

Install the development requirements and run the test suite:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

The project currently has 15 automated tests. They cover the required endpoints, validation rules, status codes, JSON errors, OpenAPI responses and the empty `204` delete response.

## Expected reset behaviour

This project does not use a database or file storage. If the server is stopped and started again, tasks created during the previous run are removed and the original three sample tasks return. This is expected for this assignment.

## Author

Md. Tamjid Hossain

FlyRank AI Internship — Backend Track, Week 2
