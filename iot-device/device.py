import os
import time
import requests
from datetime import datetime

device_name = os.getenv("DEVICE_NAME", "device")
controller_url = "http://iot-server:8080/data"

while True:
    temp = 25 + 5 * (time.time() % 10)
    timestamp = datetime.utcnow().isoformat()

    print(f"[{device_name}] {timestamp} - Reporting temperature: {temp:.2f}°C")

    payload = {
        "device": device_name,
        "temperature": temp,
        "timestamp": timestamp
    }

    try:
        response = requests.post(controller_url, json=payload)
        response.raise_for_status()
    except requests.exceptions.RequestException as e:
        print(f"[{device_name}] Error reporting to controller: {e}")

    time.sleep(5)