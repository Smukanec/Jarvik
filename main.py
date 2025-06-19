from flask import Flask, request, send_from_directory, jsonify
import requests
import os
import sys
import json
from datetime import datetime

# Pro přímý import agenta
sys.path.append(os.path.join(os.getcwd(), "agent"))
from search_agent import search_and_answer

app = Flask(__name__)

STATIC_FOLDER = os.path.join(os.getcwd(), "static")

USERNAME = "admin"
PASSWORD = "jarvik2025"

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "mistral-openorca:7b"

MEMORY_FILE = os.path.join(os.getcwd(), "memory", "log.json")
KNOWLEDGE_FOLDER = os.path.join(os.getcwd(), "knowledge")

# 🧠 Paměť: ukládání dotazů a odpovědí
def log_memory(source, question, answer):
    os.makedirs(os.path.dirname(MEMORY_FILE), exist_ok=True)
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            history = json.load(f)
    except:
        history = []

    history.append({
        "timestamp": datetime.utcnow().isoformat(),
        "source": source,
        "question": question,
        "answer": answer
    })

    with open(MEMORY_FILE, "w", encoding="utf-8") as f:
        json.dump(history, f, indent=2, ensure_ascii=False)

# 📚 Načítání znalostí ze složky `knowledge/`
def load_knowledge():
    if not os.path.isdir(KNOWLEDGE_FOLDER):
        return ""

    combined = ""
    for fname in os.listdir(KNOWLEDGE_FOLDER):
        if fname.endswith(".txt") or fname.endswith(".md"):
            path = os.path.join(KNOWLEDGE_FOLDER, fname)
            try:
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    combined += f"\n\n# {fname}\n{content}"
            except:
                continue
    return combined.strip()

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
    if not prompt:
        return jsonify({"error": "Empty message"}), 400

    try:
        knowledge_text = load_knowledge()
        full_prompt = f"Na základě následujících znalostí odpověz na dotaz:\n{knowledge_text}\n\nDotaz: {prompt}"

        response = requests.post(OLLAMA_URL, json={
            "model": OLLAMA_MODEL,
            "prompt": full_prompt,
            "stream": False
        }, timeout=30)

        if response.status_code == 200:
            content = response.json().get("response", "").strip()
            log_memory("mistral", prompt, content)
            return jsonify({"response": content})
        else:
            return jsonify({"error": f"Ollama error: {response.text}"}), 500
    except Exception as e:
        return jsonify({"error": f"Výjimka: {str(e)}"}), 500

@app.route("/search", methods=["POST"])
def search():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No data provided"}), 400

    if data.get("username") != USERNAME or data.get("password") != PASSWORD:
        return jsonify({"error": "Invalid credentials"}), 403

    question = data.get("message", "").strip()
    if not question:
        return jsonify({"error": "Empty question"}), 400

    try:
        answer = search_and_answer(question)
        log_memory("search", question, answer)
        return jsonify({"response": answer})
    except Exception as e:
        return jsonify({"error": f"Výjimka při hledání: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(host="::", port=8000)
