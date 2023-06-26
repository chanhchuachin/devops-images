import time
from celery import Celery

print(__name__)
# app = Celery('tasks', broker='redis://:123456@192.168.1.212:6379//', backend="redis://:123456@192.168.1.212:6379/0")

# @app.task
# def add(x, y):
#     time.sleep(2)
#     return x + y