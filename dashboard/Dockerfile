FROM python:3.12-slim

RUN pip install --no-cache-dir flask flask-socketio eventlet flask-cors

WORKDIR /app

COPY app.py .

EXPOSE 5002

CMD ["python", "-u", "app.py"]