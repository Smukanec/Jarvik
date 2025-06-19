#!/bin/bash

echo "🧠 Instalace Jarvika – start"

# Vytvoření virtuálního prostředí
echo "📦 Vytvářím venv..."
python3 -m venv venv

# Aktivace venv
source venv/bin/activate

# Instalace Python knihoven
echo "📚 Instaluji requirements..."
pip install -r requirements.txt

# Vytvoření složek, pokud neexistují
mkdir -p memory knowledge

echo "✅ Hotovo. Spusť Jarvika pomocí:"
echo "source venv/bin/activate && flask --app main.py run --host=:: --port=8000"
