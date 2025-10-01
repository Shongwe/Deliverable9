FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpcap-dev \
        tcpdump \
        iproute2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        flask \
        requests \
        scapy \
        joblib \
        scikit-learn \
        pandas

COPY rf_gotham_ddos.pkl /app/model.pkl
COPY detect_syn.py /app/detect_syn.py
COPY iot_server.py /app/iot_server.py

WORKDIR /app

EXPOSE 8080

CMD ["sh", "-c", "python3 detect_syn.py & python3 iot_server.py"]
