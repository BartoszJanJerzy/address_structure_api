FROM python:3.11-slim


RUN ["python3", "-m", "pip", "install", "--upgrade", "pip"]
COPY requirements.txt requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]


COPY src/backend src/backend
COPY src/common src/common
COPY resources resources


CMD ["celery", "-A", "src.backend.celery_app", "worker", "--loglevel=info", "--autoscale=100,10"]