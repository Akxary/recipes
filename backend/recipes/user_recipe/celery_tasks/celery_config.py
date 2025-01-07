from celery import Celery

from recipes.settings import RedisConfig


celery_app = Celery(
    "tasks",
    broker=RedisConfig.url(),
    include=[
        "user_recipe.celery_tasks.tasks",
        # "app.tasks.scheduled"
    ],
)
