import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import logging
from datetime import datetime
from collections import defaultdict
import subprocess

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

alerts = []
alert_counts = defaultdict(int)
blocked_ips = set()

metrics = {
    "totalPackets": 0,
    "suspiciousEvents": 0,
    "blockedIPs": 0,
    "activeConnections": 0,
    "ddosAlerts": 0
}

@app.route('/')
def index():
    return "Dashboard is running."

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.get_json()
    source_ip = data.get("source_ip")
    destination_ip = data.get("destination_ip")

    if 'type' in data and data['type'] in ['SYN Flood', 'Benign', 'Port Scan', 'DoS']:
        data['timestamp'] = datetime.utcnow().isoformat()
        logging.info(f"[Network Alert] {data}")
        alerts.append(data)

        metrics["totalPackets"] += 1
        if data['type'] != "Benign":
            metrics["suspiciousEvents"] += 1
        if data['type'] == "SYN Flood":
            metrics["ddosAlerts"] += 1

        if source_ip:
            alert_counts[source_ip] += 1
            if alert_counts[source_ip] >= 1000 and source_ip not in blocked_ips:
                block_ip(source_ip)
                blocked_ips.add(source_ip)
                metrics["blockedIPs"] += 1
                socketio.emit("blocked_ip", {"ip": source_ip})
                logging.warning(f"[BLOCKED] {source_ip} after 1000 SYN Flood alerts")

        socketio.emit('new_alert', data)
        return jsonify({"status": "network alert received"}), 200
    else:
        logging.debug(f"[Ignored] Non-network alert: {data}")
        return jsonify({"status": "ignored"}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts), 200

@app.route('/metrics', methods=['GET'])
def get_metrics():
    return jsonify(metrics), 200

@socketio.on('connect')
def handle_connect():
    metrics["activeConnections"] += 1
    logging.info(f"Client connected. Active: {metrics['activeConnections']}")

@socketio.on('disconnect')
def handle_disconnect():
    metrics["activeConnections"] = max(0, metrics["activeConnections"] - 1)
    logging.info(f"Client disconnected. Active: {metrics['activeConnections']}")

def block_ip(ip):
    try:
        subprocess.run(["iptables", "-A", "INPUT", "-s", ip, "-j", "DROP"], check=True)
        logging.info(f"IP {ip} blocked via iptables.")
    except Exception as e:
        logging.error(f"Failed to block IP {ip}: {e}")

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)