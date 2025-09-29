# simple temperature sensor generator
import os, time, random, requests, socket
from datetime import datetime

COLLECTOR_HOST = os.environ.get("COLLECTOR_HOST", "iot-server")
COLLECTOR_PORT = int(os.environ.get("COLLECTOR_PORT", "8080"))
DEVICE_PREFIX = os.environ.get("DEVICE_PREFIX", "device")
INTERVAL = float(os.environ.get("INTERVAL", "2.0"))
BASE_TEMP = float(os.environ.get("BASE_TEMP", "22.0"))
TEMP_VARIANCE = float(os.environ.get("TEMP_VARIANCE", "0.5"))
BURST = os.environ.get("BURST", "false").lower() in ("1","true","yes")
BURST_RATE = int(os.environ.get("BURST_RATE", "40"))
BURST_DURATION = int(os.environ.get("BURST_DURATION", "5"))

try:
    DEVICE_ID = os.environ.get("DEVICE_ID") or socket.gethostname()
except Exception:
    DEVICE_ID = f"{DEVICE_PREFIX}-{random.randint(1000,9999)}"

def send_telemetry(temp, extra=None):
    url = f"http://{COLLECTOR_HOST}:{COLLECTOR_PORT}/telemetry"
    payload = {
        "timestamp": datetime.utcnow().isoformat(),
        "device_id": DEVICE_ID,
        "temperature": round(temp, 3),
        "meta": extra or {}
    }
    try:
        requests.post(url, json=payload, timeout=2)
    except Exception as e:
        print("POST error:", e)

def short_burst(rate_per_second=40, duration_s=5):
    print(f"{DEVICE_ID}: starting burst {rate_per_second}pps for {duration_s}s")
    interval = 1.0 / rate_per_second
    end = time.time() + duration_s
    while time.time() < end:
        temp = BASE_TEMP + random.gauss(0, TEMP_VARIANCE)
        send_telemetry(temp, extra={"burst": True})
        time.sleep(max(0.0001, interval))

if __name__ == "__main__":
    loop = 0
    while True:
        loop += 1
        temp = BASE_TEMP + random.gauss(0, TEMP_VARIANCE)
        # tiny chance of an anomaly spike
        if random.random() < 0.001:
            temp += random.choice([15, -15])
            send_telemetry(temp, extra={"anomaly": "spike"})
        else:
            send_telemetry(temp)
        if BURST and loop == 10:
            short_burst(BURST_RATE, BURST_DURATION)
        time.sleep(INTERVAL + random.random() * (INTERVAL / 2))
