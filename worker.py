from celery import Celery
from celery.schedules import crontab

import requests
from settings import Settings
import telegram_send

settings = Settings()

celery = Celery(broker=f"{settings.REDIS_URL}")
logger = celery.log.get_default_logger()


def send_to_telegram(arr: list):
    """
    Send telegram notifications for clients email list
    """
    for i in arr:
        telegram_send.send(messages=[f"Client with name: {i['name']}, email: {i['email']} failed task."])
        logger.info(f"User message for: {i['email']}")
    return True


def get_clients_info(clients: set):
    """
    Get name, email from the clients set ids
    """
    black_list = []
    for client in clients:
        response = requests.get(f"https://jsonplaceholder.typicode.com/users/{client}").json()
        data = {"name": response["name"], "email": response["email"]}
        logger.info(f"User info: {data}")
        black_list.append(data)
    return black_list


@celery.task
def send_notifictions():
    """
    Send notifications about clients with failed tasks
    """
    logger.info(f"Start send notifications for failed tasks")
    response = requests.get("https://jsonplaceholder.typicode.com/todos").json()
    # falsed = tuple(client for client in response if client["completed"] == False)
    falsed = [client["userId"] for client in response if client["completed"]== False]
    clients = set(falsed)
    clients_list = get_clients_info(clients)
    send_telegram = send_to_telegram(clients_list)
    logger.info(f"Done send notifications for failed tasks")


celery.conf.beat_schedule = {
    "every-1-minute": {
        "task": "worker.send_notifictions",
        "schedule": crontab(minute='*/1'),
        #"args": ("every 200 secs",),
    }
}