from celery import Celery # type: ignore

from recipes.settings import RedisConfig


celery_app = Celery(
    "tasks",
    broker=RedisConfig.url(),
    include=[
        "celery_tasks.tasks",
        # "app.tasks.scheduled"
    ],
    broker_connection_retry_on_startup=True,
)
