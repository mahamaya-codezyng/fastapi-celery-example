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
from fastapi import FastAPI, BackgroundTasks
from celery.result import AsyncResult
from tasks import generate_image, celery_app

app = FastAPI()

# Array of items to generate images for
items = [
    "Pink furry coat with a plush texture, open front, and long sleeves.",
    "High-waisted, wide-leg pink tailored trousers.",
    "Knee-length red dress with white abstract patterns and a belt at the waist."
]


@app.post("/generate-images/")
def generate_images():
    """
    Submit tasks to generate images for each item in the items array.
    """
    task_ids = []
    for item in items:
        print("tasks will be sent")
        task = generate_image.delay(item)  # Submit task to Celery
        print(task.status)
        print(f"tasks generated task : {task}, task.id: {task.id}")
        task_ids.append(task.id)  # Collect task IDs
    
    return {"message": "Image generation tasks have been submitted.", "task_ids": task_ids}


@app.get("/generate-images/status/{task_id}")
def get_task_status(task_id: str):
    """
    Check the status of an image generation task.
    """
    task_result = AsyncResult(task_id, app=celery_app)
    print("task picked up")
    print(task_result.state) 
    if task_result.state == "SUCCESS":
        return {
            "task_id": task_id,
            "status": task_result.state,
            "result": task_result.result
        }
    elif task_result.state == "FAILURE":
        return {
            "task_id": task_id,
            "status": task_result.state,
            "error": str(task_result.result)
        }
    else:
        return {
            "task_id": task_id,
            "status": task_result.state
        }

@app.get("/get-images/")
def get_images(task_ids: list[str]):
    """
    Retrieve the images generated for the given task IDs.
    """
    results = []
    for task_id in task_ids:
        task_result = AsyncResult(task_id, app=celery_app)
        if task_result.state == "SUCCESS":
            results.append({"task_id": task_id, "image_url": task_result.result})
        else:
            results.append({"task_id": task_id, "status": task_result.state})
    
    return {"images": results}
