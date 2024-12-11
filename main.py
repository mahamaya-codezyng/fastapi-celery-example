# from fastapi import FastAPI
# from tasks import long_running_task

# app = FastAPI()

# @app.post("/run-task")
# async def run_task(x: int, y: int):
#     # Trigger the Celery task
#     task = long_running_task.delay(x, y)
#     return {"task_id": task.id}

# @app.get("/task-status/{task_id}")
# async def get_task_status(task_id: str):
#     # Check the task status
#     result = long_running_task.AsyncResult(task_id)
#     if result.state == "PENDING":
#         return {"task_id": task_id, "status": "Task is still processing"}
#     elif result.state == "SUCCESS":
#         return {"task_id": task_id, "status": "Task completed", "result": result.result}
#     else:
#         return {"task_id": task_id, "status": result.state}

from fastapi import FastAPI
from tasks import generate_image

app = FastAPI()

# Array of items to generate images for
items = [
    "Pink furry coat with a plush texture, open front, and long sleeves.",
    "High-waisted, wide-leg pink tailored trousers.",
    "Knee-length red dress with white abstract patterns and a belt at the waist."
]

@app.post("/run-task")
async def run_task():
    # Trigger the Celery task
    task_ids = []
    for item in items:
        task = generate_image.delay(item)  # Submit task to Celery
        task_ids.append(task.id)  # Collect task IDs
    
    return {"message": "Image generation tasks have been submitted.", "task_ids": task_ids}

@app.get("/task-status/{task_id}")
async def get_task_status(task_id: str):
    # Check the task status
    result = generate_image.AsyncResult(task_id)
    if result.state == "PENDING":
        return {"task_id": task_id, "status": "Task is still processing"}
    elif result.state == "SUCCESS":
        return {"task_id": task_id, "status": "Task completed", "result": result.result}
    else:
        return {"task_id": task_id, "status": result.state}
