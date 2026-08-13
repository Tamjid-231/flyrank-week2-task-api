from fastapi import FastAPI


app = FastAPI(title="Task API", version="1.0.0")


@app.get("/", summary="Describe the API")
def api_information():
    return {"name": "Task API", "version": "1.0", "endpoints": ["/tasks"]}


@app.get("/health", summary="Check server health")
def health_check():
    return {"status": "ok"}
