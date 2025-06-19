import requests
from bs4 import BeautifulSoup

def search_and_answer(query):
    try:
        url = f"https://html.duckduckgo.com/html/?q={query.replace(" ", "+")}"
        headers = {"User-Agent": "JarvikBot/1.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            results = soup.find_all("a", {"class": "result__a"}, limit=3)
            summary = "
".join([r.get_text(strip=True) for r in results])
            return summary if summary else "Nic relevantního nebylo nalezeno."
        else:
            return "Web search selhal."
    except Exception as e:
        return f"Chyba při hledání: {str(e)}"
