from __future__ import absolute_import
from celery import Celery
import os
import statsd


rabbit_url = os.getenv("RABBITHOST", "localhost")

app = Celery(
    "celery_app",
    broker=f"amqp://guest:guest@{rabbit_url}:5672",
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
