
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin

BASE = "https://tv.apple.com"
URL = BASE + "/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def main():
    print("=" * 60)
    print("BUSCANDO RUTAS DE TEMPORADAS Y EPISODIOS")
    print("=" * 60)

    try:
        respuesta = requests.get(URL, headers=HEADERS, timeout=30)
        respuesta.raise_for_status()

        html = respuesta.text
        soup = BeautifulSoup(html, "html.parser")

        print("\n1. ENLACES DE TEMPORADAS Y EPISODIOS")

        enlaces = set()

        for elemento in soup.find_all(["a", "option"]):
            href = elemento.get("href")

            if href:
                texto = elemento.get_text(" ", strip=True)

                if any(p in (href + texto).lower()
                       for p in ["season", "episode"]):
                    enlaces.add((texto, urljoin(URL, href)))

        if enlaces:
            for texto, enlace in sorted(enlaces):
                print(texto, "->", enlace)
        else:
            print("No se encontraron enlaces directos.")

        print("\n2. IDENTIFICADORES APPLE DE CONTENIDO")

        ids = sorted(set(re.findall(
            r"umc\.cmc\.[a-zA-Z0-9]+",
            html
        )))

        for identificador in ids[:40]:
            print(identificador)

        print("\n3. RUTAS DEL JAVASCRIPT")

        script_url = urljoin(
            BASE,
            "/assets/main~Bel1jRMkHC.js"
        )

        js_respuesta = requests.get(
            script_url,
            headers=HEADERS,
            timeout=30
        )
        js_respuesta.raise_for_status()

        js = js_respuesta.text

        patrones = [
            r'[^"\'\s]{0,100}SeasonPageIntent[^"\'\s]{0,150}',
            r'[^"\'\s]{0,100}BoxSetEpisodesPaginationIntent[^"\'\s]{0,150}',
            r'[^"\'\s]{0,100}EpisodePageIntent[^"\'\s]{0,150}',
            r'[^"\'\s]{0,100}seasonNumber[^"\'\s]{0,150}',
            r'[^"\'\s]{0,100}episodeNumber[^"\'\s]{0,150}'
        ]

        for patron in patrones:
            resultados = re.findall(patron, js, re.I)
            print("\nCoincidencias:", len(resultados))

            for resultado in resultados[:3]:
                print(resultado[:250])

        print("\n4. DATOS DE TEMPORADAS EN HTML")

        for opcion in soup.find_all("option"):
            texto = opcion.get_text(" ", strip=True)
            if "season" in texto.lower():
                print(texto)

        print("\nPRUEBA TERMINADA.")

    except Exception as error:
        print("ERROR:", repr(error))


if __name__ == "__main__":
    main()
