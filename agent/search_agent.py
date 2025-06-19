import requests
from bs4 import BeautifulSoup

OLLAMA_URL = "http://localhost:11434/api/generate"
OLLAMA_MODEL = "tinyllama"

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}

def duckduckgo_search(query):
    url = f"https://html.duckduckgo.com/html/?q={query}"
    res = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(res.text, "html.parser")
    links = soup.select(".result__url")
    if links:
        href = links[0].get("href")
        return href
    return None

def fetch_page_text(url):
    try:
        res = requests.get(url, headers=HEADERS, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        texts = soup.find_all("p")
        return "\n".join([p.get_text() for p in texts])[:4000]
    except:
        return ""

def ask_tinyllama(prompt):
    payload = {
        "model": OLLAMA_MODEL,
        "prompt": prompt,
        "stream": False
    }
    res = requests.post(OLLAMA_URL, json=payload, timeout=30)
    return res.json().get("response", "").strip()

def search_and_answer(question):
    print(f"Hledám odpověď na: {question}")
    link = duckduckgo_search(question)
    if not link:
        return "Nepodařilo se najít žádný relevantní odkaz."
    content = fetch_page_text(link)
    if not content:
        return f"Nepodařilo se načíst obsah stránky: {link}"
    prompt = f"Odpověz na otázku: '{question}' na základě následujícího textu:\n\n{content}"
    answer = ask_tinyllama(prompt)
    return f"🔗 {link}\n\n📄 {answer}"
