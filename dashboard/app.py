from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/api/status', methods=['GET'])
def status():
    return jsonify({"status": "Dashboard is live", "timestamp": request.args.get("ts", "none")})

@app.route('/api/alerts', methods=['POST'])
def alerts():
    data = request.get_json()
    return jsonify({"received": data}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)