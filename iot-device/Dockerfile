FROM python:3.10-slim

RUN apt-get update && \
    apt-get install -y curl iputils-ping && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir requests

COPY device.py /device.py

CMD ["python", "/device.py"]