FROM python:3.10-slim
WORKDIR /app
RUN pip install scapy
COPY attacker.py .
CMD ["python", "attacker.py"]