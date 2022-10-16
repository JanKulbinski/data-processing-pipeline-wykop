from __future__ import absolute_import
from celery import Celery
import os
import statsd


rabbit_url = os.getenv("RABBITHOST", "localhost")
rabbit_pass = os.getenv("RABIT_PASSWORD")
rabbit_user = os.getenv("RABIT_USER")

app = Celery(
    "celery_app",
    broker=f"amqp://{rabbit_user}:{rabbit_pass}@{rabbit_url}:5672",
    backend="rpc://",
    include=["celery_app.tasks"],
)

app.conf.beat_schedule = {
    'scrap-every-30-seconds': {
        'task': 'celery_app.tasks.scrap_wykop',
        'schedule': 30.0,
    },
}

stats = statsd.StatsClient('graphite', 8125)
