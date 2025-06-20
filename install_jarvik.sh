#!/bin/bash

# 📥 Klonování repozitáře
echo "🌀 Klonuju repozitář..."
git clone https://github.com/Smukanec/Jarvik.git ~/jarvik

# 📁 Přechod do složky
cd ~/jarvik || exit 1

# 🧰 Instalace závislostí
echo "📦 Instaluju Flask..."
pip install -r requirements.txt

# ▶️ Spuštění
echo "🚀 Spouštím Jarvika..."
python3 main.py
