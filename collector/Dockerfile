FROM python:3.11-slim

# Install tcpdump and tshark for capture/analysis
RUN apt-get update && apt-get install -y tcpdump tshark && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY server.py /app/server.py

EXPOSE 8080

# Entrypoint: start packet capture in background and then the HTTP server
CMD bash -lc "tcpdump -i any -w /captures/iot_capture.pcap & python server.py"
