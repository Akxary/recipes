FROM python:3.11-alpine as builder
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /app
COPY requirements.txt /app/
RUN pip wheel --no-cache-dir --no-deps -r requirements.txt -w /wheels

FROM python:3.11-alpine
WORKDIR /app
COPY --from=builder /wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels /wheels/*

COPY pyproject.toml pyproject.toml
COPY recipes /app/recipes/
WORKDIR /app/recipes
CMD ["sh", "-c", "python manage.py migrate && gunicorn recipes.wsgi:application --bind 0.0.0.0:8000 --workers 1"]
