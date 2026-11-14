
import requests
import re
import json
from bs4 import BeautifulSoup

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}

def buscar_contexto(texto, patrones, limite=5):
    encontrados = 0

    for patron in patrones:
        for coincidencia in re.finditer(patron, texto, re.I):
            inicio = max(0, coincidencia.start() - 250)
            fin = min(len(texto), coincidencia.end() + 500)

            print("\n" + "-" * 60)
            print(texto[inicio:fin])
            encontrados += 1

            if encontrados >= limite:
                return

    if encontrados == 0:
        print("No se encontraron coincidencias.")

def main():
    print("=" * 60)
    print("DIAGNÓSTICO DE APPLE TV")
    print("=" * 60)

    try:
        respuesta = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        print("Estado HTTP:", respuesta.status_code)
        print("Bytes recibidos:", len(respuesta.content))

        respuesta.raise_for_status()

        respuesta.encoding = respuesta.apparent_encoding
        html = respuesta.text

        soup = BeautifulSoup(html, "html.parser")

        print("\n1. TÍTULO")
        print(soup.title.get_text(strip=True) if soup.title else "No encontrado")

        print("\n2. METADATOS")
        for meta in soup.find_all("meta"):
            nombre = meta.get("property") or meta.get("name")
            contenido = meta.get("content")

            if nombre and contenido:
                if any(x in nombre.lower() for x in [
                    "title", "description", "episode", "season"
                ]):
                    print(nombre, "=", contenido)

        print("\n3. DATOS JSON-LD")
        json_ld = soup.find_all(
            "script",
            type="application/ld+json"
        )

        if json_ld:
            for script in json_ld:
                print((script.string or script.get_text())[:5000])
        else:
            print("No se encontró JSON-LD.")

        print("\n4. SCRIPTS DE LA PÁGINA")
        for script in soup.find_all("script", src=True):
            print(script.get("src"))

        print("\n5. BUSCANDO TEMPORADAS Y EPISODIOS")

        patrones = [
            r"season",
            r"episode",
            r"Two and a Half Men",
            r"episodeNumber",
            r"seasonNumber",
            r"tvSeason",
            r"tvEpisode",
            r"adamId"
        ]

        buscar_contexto(html, patrones, limite=12)

        print("\n6. RESULTADO")
        print("Diagnóstico terminado.")

    except Exception as error:
        print("ERROR:", repr(error))

if __name__ == "__main__":
    main()
