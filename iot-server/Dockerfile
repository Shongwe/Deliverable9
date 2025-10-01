FROM python:3.9-slim

WORKDIR /app

COPY iot_server.py .

RUN pip install --no-cache-dir flask requests


EXPOSE 8080

CMD ["python", "iot_server.py"]