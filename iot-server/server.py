from flask import Flask, request, jsonify
import logging
import requests

app = Flask(__name__)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

@app.route('/data', methods=['POST'])
def receive_data():
    data = request.get_json()
    logging.info(f"Received sensor data: {data}")

    try:
        response = requests.post("http://dashboard:5002/alert", json=data)
        response.raise_for_status()
        logging.info("Forwarded to dashboard successfully.")
    except requests.exceptions.RequestException as e:
        logging.error(f"Failed to forward to dashboard: {e}")

    return jsonify({"status": "Data received", "data": data}), 200

@app.route('/', methods=['GET'])
def home():
    return jsonify({"status": "IoT Server Running"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)