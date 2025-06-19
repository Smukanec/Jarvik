#!/bin/bash
echo "🧹 Zastavuji a odstraňuji systemd služby Jarvika..."
systemctl --user stop jarvik.service
systemctl --user stop mistral.service
systemctl --user stop tinyllama.service
systemctl --user stop gemma.service
systemctl --user disable jarvik.service
systemctl --user disable mistral.service
systemctl --user disable tinyllama.service
systemctl --user disable gemma.service
rm -f ~/.config/systemd/user/jarvik.service
rm -f ~/.config/systemd/user/mistral.service
rm -f ~/.config/systemd/user/tinyllama.service
rm -f ~/.config/systemd/user/gemma.service
systemctl --user daemon-reload
echo "✅ Vše odstraněno. Jarvikovy služby už neběží a nespustí se po restartu."
