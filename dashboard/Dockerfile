FROM python:3.12-slim

RUN pip install --no-cache-dir flask flask-socketio eventlet jsonify logging

WORKDIR /app

COPY app.py .

CMD ["python", "-u", "app.py"]