from http.server import BaseHTTPRequestHandler, HTTPServer
import logging, json, os
from datetime import datetime

LOG_DIR = "/app/logs"
os.makedirs(LOG_DIR, exist_ok=True)
LOG_FILE = os.path.join(LOG_DIR, "telemetry.log")
CSV_FILE = os.path.join(LOG_DIR, "telemetry.csv")

class Handler(BaseHTTPRequestHandler):
    def _write_csv(self, data):
        header = "timestamp,device_id,temperature,extra\n"
        if not os.path.exists(CSV_FILE):
            with open(CSV_FILE,"w") as f:
                f.write(header)
        row = f"{data.get('timestamp')},{data.get('device_id')},{data.get('temperature')},{data.get('extra','')}\n"
        with open(CSV_FILE,"a") as f:
            f.write(row)

    def do_POST(self):
        length = int(self.headers.get("Content-Length",0))
        body = self.rfile.read(length) if length else b''
        try:
            payload = json.loads(body.decode())
        except Exception:
            payload = {"raw": body.decode('utf-8', errors='ignore')}
        entry = {"received_at": datetime.utcnow().isoformat(), "client": self.client_address[0], "payload": payload}
        with open(LOG_FILE,"a") as f:
            f.write(json.dumps(entry) + "\n")
        if isinstance(payload, dict) and "device_id" in payload and "temperature" in payload:
            csv_row = {"timestamp": payload.get("timestamp"), "device_id": payload.get("device_id"), "temperature": payload.get("temperature"), "extra": json.dumps(payload.get("meta",{}))}
            self._write_csv(csv_row)
        self.send_response(200)
        self.send_header("Content-type","application/json")
        self.end_headers()
        self.wfile.write(json.dumps({"status":"ok"}).encode())

    def do_GET(self):
        if self.path.startswith("/status"):
            self.send_response(200)
            self.send_header("Content-type","application/json")
            self.end_headers()
            self.wfile.write(json.dumps({"status":"running"}).encode())
        else:
            self.send_response(404)
            self.end_headers()

if __name__=="__main__":
    logging.basicConfig(level=logging.INFO)
    httpd = HTTPServer(("0.0.0.0",8080), Handler)
    logging.info("Collector running on 0.0.0.0:8080")
    httpd.serve_forever()
