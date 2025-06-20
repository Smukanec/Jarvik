from flask import Flask, request, jsonify, send_from_directory
import requests

OLLAMA_HOST = "http://localhost:11434"

app = Flask(__name__, static_folder='static')

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    message = data.get("message")
    model = data.get("model")
    user = data.get("user", "user")

    payload = {
        "model": model,
        "messages": [
            {"role": "system", "content": f"Uživatel: {user}"},
            {"role": "user", "content": message}
        ],
        "stream": False
    }

    try:
        res = requests.post(f"{OLLAMA_HOST}/api/chat", json=payload)
        res.raise_for_status()
        response = res.json().get("message", {}).get("content", "[Žádná odpověď]")
    except Exception as e:
        response = f"[Chyba komunikace s modelem: {str(e)}]"

    return jsonify({"response": response})

@app.route('/start', methods=['POST'])
def start():
    data = request.get_json()
    model = data.get("model")
    # Načte model (pull, pokud není) – Ollama API to zvládne samo
    try:
        res = requests.post(f"{OLLAMA_HOST}/api/show", json={"name": model})
        if res.status_code != 200:
            requests.post(f"{OLLAMA_HOST}/api/pull", json={"name": model})
    except:
        pass
    return jsonify({"status": f"Model {model} připraven"})

@app.route('/stop', methods=['POST'])
def stop():
    return jsonify({"status": "stop ignorováno – Ollama API běží stále"})

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)