
from flask import Flask, request, jsonify
import subprocess

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    model = data.get("model")
    user = data.get("user")
    response = subprocess.run(
        ["ollama", "run", model, "--prompt", message],
        capture_output=True, text=True
    )
    return jsonify({"response": response.stdout.strip()})

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    model = data.get("model")
    subprocess.Popen(["bash", f"scripts/start_{model}.sh"])
    return jsonify({"status": "started"})

@app.route('/stop', methods=['POST'])
def stop():
    data = request.get_json()
    model = data.get("model")
    subprocess.run(["bash", f"scripts/stop_{model}.sh"])
    return jsonify({"status": "stopped"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)
