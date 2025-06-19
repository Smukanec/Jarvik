from flask import Flask, request, send_from_directory, jsonify
import requests
import os
import json
from agent.search_agent import search_and_answer

app = Flask(__name__)
STATIC_FOLDER = os.path.join(os.getcwd(), "static")

USERNAME = "admin"
PASSWORD = "jarvik2025"

OLLAMA_URL = "http://localhost:11434/api/generate"
DEFAULT_MODEL = "mistral-openorca:7b"
GEMMA_MODEL = "gemma:2b"

MEMORY_FILE = os.path.join("memory", "log.json")

def append_to_memory(prompt, response):
    os.makedirs("memory", exist_ok=True)
    history = []
    if os.path.exists(MEMORY_FILE):
        with open(MEMORY_FILE, "r") as f:
            try:
                history = json.load(f)
            except json.JSONDecodeError:
                history = []

    history.extend([
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": response}
    ])

    with open(MEMORY_FILE, "w") as f:
        json.dump(history, f, indent=2)

def generate_response(prompt, model=DEFAULT_MODEL):
    try:
        response = requests.post(OLLAMA_URL, json={
            "model": model,
            "prompt": prompt,
            "stream": False
        }, timeout=60)
        if response.status_code == 200:
            return response.json().get("response", "").strip()
        else:
            return f"Ollama chyba: {response.text}"
    except Exception as e:
        return f"Výjimka: {str(e)}"

@app.route("/")
def index():
    return send_from_directory(STATIC_FOLDER, "index.html")

@app.route("/<path:path>")
def serve_static(path):
    return send_from_directory(STATIC_FOLDER, path)

@app.route("/ask", methods=["POST"])
def ask():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400
    if data.get("username") != USERNAME or data.get("password") != PASSWORD:
        return jsonify({"error": "Invalid credentials"}), 403

    prompt = data.get("message", "").strip()
    mode = data.get("mode", "mistral")
    model_map = {
        "mistral": DEFAULT_MODEL,
        "gemma": GEMMA_MODEL
    }

    if not prompt:
        return jsonify({"error": "Empty message"}), 400

    if mode == "search":
        result = search_and_answer(prompt)
        append_to_memory(prompt, result)
        return jsonify({"response": result})
    else:
        model = model_map.get(mode, DEFAULT_MODEL)
        result = generate_response(prompt, model)
        append_to_memory(prompt, result)
        return jsonify({"response": result})

if __name__ == "__main__":
    app.run(host="::", port=8000)
