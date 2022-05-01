FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

COPY ./app /app
WORKDIR /app
RUN pip install --upgrade pip --no-cache-dir
RUN pip install -r requirements.txt --no-cache-dir

