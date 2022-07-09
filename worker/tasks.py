from celery import Celery
from celery.schedules import crontab 

celery = Celery(broker="redis://:pyVHRTDeEZMFbEVR3qhTnXf9KAGLlxhI@redis-16247.c302.asia-northeast1-1.gce.cloud.redislabs.com:16247")
logger = celery.log.get_default_logger()

@celery.task
def test_task(timing):
    logger.info(f"test task: {timing}")


celery.conf.beat_schedule = {
    "every-1-minute": {
        "task": "tasks.test_task",
        "schedule": 15,
        "args": ("every 15 secs",),
    }
}