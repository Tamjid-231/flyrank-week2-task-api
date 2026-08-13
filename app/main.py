from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from pydantic import BaseModel, field_validator


app = FastAPI(title="Task API", version="1.0.0")


class Task(BaseModel):
    id: int
    title: str
    done: bool


class TaskCreate(BaseModel):
    title: str

    @field_validator("title")
    @classmethod
    def title_must_not_be_empty(cls, value: str):
        if not value.strip():
            raise ValueError("title must not be empty")
        return value.strip()


tasks = [
    {"id": 1, "title": "Read the assignment", "done": True},
    {"id": 2, "title": "Build the CRUD API", "done": False},
    {"id": 3, "title": "Test it in Swagger UI", "done": False},
]


def find_task(task_id: int):
    return next((task for task in tasks if task["id"] == task_id), None)


@app.exception_handler(RequestValidationError)
async def validation_error_handler(request: Request, exc: RequestValidationError):
    first_error = exc.errors()[0]
    message = first_error.get("msg", "Invalid request body")
    return JSONResponse(status_code=400, content={"error": message})


@app.get("/", summary="Describe the API")
def api_information():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Check server health")
def health_check():
    return {"status": "ok"}


@app.get("/tasks", response_model=list[Task], summary="List all tasks")
def list_tasks():
    return tasks


@app.get("/tasks/{task_id}", response_model=Task, summary="Get one task")
def get_task(task_id: int):
    task = find_task(task_id)
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"},
        )
    return task


@app.post("/tasks", response_model=Task, status_code=201, summary="Create a task")
def create_task(task_data: TaskCreate):
    next_id = max((task["id"] for task in tasks), default=0) + 1
    new_task = {"id": next_id, "title": task_data.title, "done": False}
    tasks.append(new_task)
    return new_task
