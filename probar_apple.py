
import requests
import json
from bs4 import BeautifulSoup

URL = "https://tv.apple.com/fr/episode/pilot/umc.cmc.3w9dbmyr33eubzq38cb6zi8nx?showId=umc.cmc.4syd3ylis0va9bpj1y923v20g&l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def main():
    print("=" * 60)
    print("ANÁLISIS DE FICHA INDIVIDUAL")
    print("=" * 60)

    try:
        response = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        response.raise_for_status()

        response.encoding = response.apparent_encoding

        soup = BeautifulSoup(response.text, "html.parser")

        print("\n1. TÍTULO")
        print(
            soup.title.get_text(strip=True)
            if soup.title else "No encontrado"
        )

        print("\n2. METADATOS")
        for meta in soup.find_all("meta"):
            name = meta.get("property") or meta.get("name")
            content = meta.get("content")

            if name and content:
                print(name, "=", content)

        print("\n3. JSON-LD")
        scripts = soup.find_all(
            "script",
            type="application/ld+json"
        )

        for script in scripts:
            content = script.string or script.get_text()

            try:
                data = json.loads(content)
                print(json.dumps(
                    data,
                    indent=2,
                    ensure_ascii=False
                ))
            except json.JSONDecodeError:
                print(content[:5000])

        print("\n4. INFORMACIÓN DE TEMPORADA Y EPISODIO")

        for palabra in [
            "seasonNumber",
            "episodeNumber",
            "Season 1",
            "Episode 1",
            "Pilot"
        ]:
            print(
                palabra,
                "->",
                palabra.lower() in response.text.lower()
            )

        print("\n5. TEXTO DE LA PÁGINA")
        print(soup.get_text(" ", strip=True)[:5000])

        print("\nPRUEBA TERMINADA.")

    except Exception as error:
        print("ERROR:", repr(error))


if __name__ == "__main__":
    main()
