# Jarvik – AI pomocník s lokální pamětí

Jarvik je jednoduchý lokální AI asistent postavený na Flasku a Mistralu (Ollama), navržený pro provoz bez nutnosti internetu. Může sloužit jako vlastní offline ChatGPT s přístupem do internetu přes plugin, pokud je aktivní.

## Funkce
- Rozhraní přes prohlížeč (`/`)
- API endpoint `/ask`
- Heslo: `admin / jarvik2025`
- Využívá jazykový model Mistral (`ollama run mistral-openorca:7b`)
- Umožňuje dotazy s přístupem do internetu (plugin)
- Zelený text na černém pozadí (viz `static/styles.css`)
- Možnost napojení na ChatGPT jako externí API

## Spuštění

### 1. Aktivace prostředí
```bash
cd ~/jarvik
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### 2. Spuštění Flask serveru
```bash
flask --app main.py run --host=:: --port=8000
```

### 3. Přístup přes:
- Web: `http://localhost:8000`
- IPv6: `http://[tvoje_IPv6]:8000`
- API POST `/ask`

### 4. Volání API:
```bash
curl -X POST http://localhost:8000/ask \
     -H "Content-Type: application/json" \
     -d '{"username":"admin","password":"jarvik2025","message":"Kdo je prezident?"}'
```

## Struktura složek
```
jarvik/
├── main.py
├── requirements.txt
├── static/
│   ├── index.html
│   └── styles.css
├── memory/             ← JSON soubory s pamětí
├── knowledge/          ← Znalostní databáze
```

---

## Předpoklady
- Python 3.9+
- Ollama nainstalována (`ollama run mistral-openorca:7b`)
