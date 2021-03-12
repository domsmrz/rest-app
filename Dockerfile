FROM python:3.8-slim-buster

WORKDIR /app/
COPY . .

RUN pip install -r /app/requirements.txt

EXPOSE 8000

CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:8000", "-t", "600", "rest_app:create_app()", "--preload"]
