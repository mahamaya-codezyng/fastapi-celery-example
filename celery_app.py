from celery import Celery
from tasks import generate_image  # Ensure tasks are registered

# Configure Celery
celery_app = Celery(
    "fastapi-celery-example",
    broker="redis://localhost:6379/0",  # Redis broker URL
    backend="redis://localhost:6379/0"  # Redis result backend URL
)

# Celery configuration
celery_app.conf.update(
    task_routes={
        'tasks.generate_image': {'queue': 'image_generation'},
    },
    task_time_limit=30,  # Ensure tasks are killed after 30 seconds
    worker_concurrency=3  # Configure a single worker with 3 processes
)
