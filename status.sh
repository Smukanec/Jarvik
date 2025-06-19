#!/bin/bash
echo "🔍 Stav systemd služeb Jarvika:"
systemctl --user is-active mistral.service >/dev/null && echo "🧠 Mistral:      ✅ běží" || echo "🧠 Mistral:      ❌ neběží"
systemctl --user is-active gemma.service >/dev/null && echo "🧠 Gemma:        ✅ běží" || echo "🧠 Gemma:        ❌ neběží"
systemctl --user is-active tinyllama.service >/dev/null && echo "🦙 TinyLlama:    ✅ běží" || echo "🦙 TinyLlama:    ❌ neběží"
systemctl --user is-active jarvik.service >/dev/null && echo "🚪 Flask server: ✅ běží" || echo "🚪 Flask server: ❌ neběží"
