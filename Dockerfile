#syntax=docker/dockerfile:1

FROM python:3.12-alpine
WORKDIR /app

COPY requirements.txt /app
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app

ENV GUNICORN_BIND=0.0.0.0:5000
ENV GUNICORN_PROCESSES=2
ENV GUNICORN_THREADS=4

EXPOSE 5000

CMD ["gunicorn", "--config", "gunicorn_config.py", "app:create_app()"]
