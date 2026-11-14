
import requests
import json
import re
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse, parse_qs

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def obtener_pagina(url):
    respuesta = requests.get(
        url,
        headers=HEADERS,
        timeout=30
    )
    respuesta.raise_for_status()
    respuesta.encoding = respuesta.apparent_encoding
    return BeautifulSoup(respuesta.text, "html.parser")


def extraer_datos_episodio(url):
    soup = obtener_pagina(url)

    for script in soup.find_all(
        "script",
        type="application/ld+json"
    ):
        try:
            datos = json.loads(
                script.string or script.get_text()
            )

            elementos = datos if isinstance(datos, list) else [datos]

            for elemento in elementos:
                if elemento.get("@type") != "Episode":
                    continue

                titulo = elemento.get("name", "")
                titulo = re.sub(
                    r"^.*? - ",
                    "",
                    titulo
                )

                temporada = elemento.get("partOfSeason")
                numero = elemento.get("episodeNumber")

                if isinstance(temporada, dict):
                    temporada = temporada.get("seasonNumber")

                if not titulo or not temporada or not numero:
                    continue

                return {
                    "temporada": int(temporada),
                    "episodio": int(numero),
                    "titulo": titulo,
                    "url": url
                }

        except (json.JSONDecodeError, TypeError, ValueError):
            continue

    return None


def main():
    print("=" * 65)
    print("EXTRACCIÓN DE EPISODIOS - APPLE TV")
    print("=" * 65)

    soup = obtener_pagina(URL)

    enlaces = {}

    for enlace in soup.find_all("a", href=True):
        href = urljoin(URL, enlace["href"])

        if "/episode/" not in urlparse(href).path:
            continue

        parametros = parse_qs(urlparse(href).query)

        if parametros.get("showId", [""])[0] != (
            "umc.cmc.4syd3ylis0va9bpj1y923v20g"
        ):
            continue

        enlaces[href] = href

    print("Enlaces de episodios encontrados:", len(enlaces))

    resultados = []

    for indice, enlace in enumerate(enlaces, 1):
        print(f"\nConsultando episodio {indice}...")

        try:
            datos = extraer_datos_episodio(enlace)

            if datos:
                resultados.append(datos)

                print(
                    f"Temporada {datos['temporada']} "
                    f"Episodio {datos['episodio']} - "
                    f"{datos['titulo']}"
                )
            else:
                print("No se encontraron metadatos.")

        except Exception as error:
            print("Error:", error)

    resultados.sort(
        key=lambda x: (x["temporada"], x["episodio"])
    )

    with open(
        "episodios_apple.json",
        "w",
        encoding="utf-8"
    ) as archivo:
        json.dump(
            resultados,
            archivo,
            ensure_ascii=False,
            indent=2
        )

    print("\n" + "=" * 65)
    print("RESULTADO")
    print("=" * 65)
    print("Episodios extraídos:", len(resultados))
    print("Archivo creado: episodios_apple.json")

    for dato in resultados:
        print(
            f"<sub-title>Temporada {dato['temporada']} "
            f"Episodio {dato['episodio']} - "
            f"{dato['titulo']}</sub-title>"
        )


if __name__ == "__main__":
    main()
