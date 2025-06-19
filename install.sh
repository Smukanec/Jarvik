#!/bin/bash
echo "🧠 Instalace Jarvika – start"
python3 -m venv venv
source venv/bin/activate
echo "📚 Instaluji requirements..."
pip install --break-system-packages -r requirements.txt || {
  echo "❌ Instalace selhala. Zkontroluj requirements.txt"
  exit 1
}
mkdir -p memory knowledge
echo "✅ Hotovo. Spusť Jarvika pomocí:"
echo "source venv/bin/activate && flask --app main.py run --host=:: --port=8000"
