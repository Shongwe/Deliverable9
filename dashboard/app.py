import eventlet
eventlet.monkey_patch()

from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
import logging

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

alerts = []

@app.route('/')
def index():
    return "Dashboard is running."

@app.route('/alert', methods=['POST'])
def receive_alert():
    data = request.get_json()

    if 'type' in data and data['type'] in ['SYN Flood', 'Benign', 'Port Scan', 'DoS']:
        logging.info(f"[Network Alert] {data}")
        alerts.append(data)
        socketio.emit('new_alert', data)
        return jsonify({"status": "network alert received"}), 200
    else:
        logging.debug(f"[Ignored] Non-network alert: {data}")
        return jsonify({"status": "ignored"}), 200

@app.route('/alerts', methods=['GET'])
def get_alerts():
    return jsonify(alerts), 200

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5002)