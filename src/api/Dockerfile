FROM python:3.11-slim

RUN ["python3", "-m", "pip", "install", "--upgrade", "pip"]
COPY requirements.txt requirements.txt
COPY src/api/requirements.txt src/api/requirements.txt
RUN ["pip", "install", "-r", "requirements.txt"]
RUN ["pip", "install", "-r", "src/api/requirements.txt"]

COPY src/api/ src/api/
COPY src/common src/common
COPY src/backend src/backend
COPY resources resources

CMD ["uvicorn", "src.api.api:app", "--host", "0.0.0.0", "--port", "1111"]