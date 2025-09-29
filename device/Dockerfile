FROM python:3.11-slim

WORKDIR /app
COPY generator.py /app/generator.py
RUN pip install --no-cache-dir requests

ENV COLLECTOR_HOST=iot-server
ENV COLLECTOR_PORT=8080
ENV DEVICE_PREFIX=device
ENV INTERVAL=2
ENV BASE_TEMP=22.0
ENV TEMP_VARIANCE=0.5
ENV BURST=false
ENV BURST_RATE=40
ENV BURST_DURATION=5

CMD ["python", "generator.py"]
