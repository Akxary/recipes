#!/bin/bash

if [ "$1" == "django" ]; then
    python manage.py migrate
    gunicorn recipes.wsgi:application --bind 0.0.0.0:8000 --workers 1
elif [ "$1" == "celery" ]; then
    celery --app=user_recipe.celery_tasks.celery_config:celery_app worker --loglevel=info
fi
