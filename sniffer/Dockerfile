FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpcap-dev \
        tcpdump \
        iproute2 \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
        scapy \
        joblib \
        scikit-learn \
        requests \
        pandas

COPY rf_gotham_ddos.pkl /app/model.pkl
COPY detect_syn.py /app/detect_syn.py

WORKDIR /app

CMD ["python", "-u", "detect_syn.py"]