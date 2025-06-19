#!/bin/bash
echo "⚙️ Nastavuji systemd služby pro Jarvika..."
mkdir -p ~/.config/systemd/user
loginctl enable-linger $USER

cat > ~/.config/systemd/user/mistral.service <<EOF
[Unit]
Description=Jarvik Mistral (Ollama)
After=network.target
[Service]
ExecStart=/usr/bin/ollama run mistral-openorca:7b
Restart=always
[Install]
WantedBy=default.target
EOF

cat > ~/.config/systemd/user/tinyllama.service <<EOF
[Unit]
Description=Jarvik TinyLlama (Ollama agent)
After=network.target
[Service]
ExecStart=/usr/bin/ollama run tinyllama
Restart=always
[Install]
WantedBy=default.target
EOF

cat > ~/.config/systemd/user/gemma.service <<EOF
[Unit]
Description=Jarvik Gemma 2B (Ollama)
After=network.target
[Service]
ExecStart=/usr/bin/ollama run gemma:2b
Restart=always
[Install]
WantedBy=default.target
EOF

cat > ~/.config/systemd/user/jarvik.service <<EOF
[Unit]
Description=Jarvik Flask Server
After=network.target
[Service]
WorkingDirectory=$HOME/jarvik
ExecStart=$HOME/jarvik/venv/bin/flask --app main.py run --host=:: --port=8000
Environment=FLASK_ENV=production
Restart=always
[Install]
WantedBy=default.target
EOF

systemctl --user daemon-reexec
systemctl --user daemon-reload
systemctl --user enable --now mistral.service
systemctl --user enable --now tinyllama.service
systemctl --user enable --now gemma.service
systemctl --user enable --now jarvik.service
echo "✅ Všechny služby spuštěny a budou automaticky startovat po rebootu."
