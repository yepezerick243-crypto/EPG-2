
import requests
import re

BASE = "https://tv.apple.com"
URL = BASE + "/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

def mostrar_coincidencias(texto, palabra, limite=5):
    posiciones = [
        m.start() for m in re.finditer(palabra, texto, re.I)
    ]

    print(f"\n'{palabra}': {len(posiciones)} coincidencias")

    for posicion in posiciones[:limite]:
        inicio = max(0, posicion - 180)
        fin = min(len(texto), posicion + 350)
        print("-" * 50)
        print(texto[inicio:fin])

def main():
    print("=" * 60)
    print("INVESTIGACIÓN DE EPISODIOS - APPLE TV")
    print("=" * 60)

    try:
        respuesta = requests.get(URL, headers=HEADERS, timeout=30)
        respuesta.raise_for_status()

        html = respuesta.text

        # Buscar el archivo JavaScript principal
        coincidencia = re.search(
            r'<script[^>]+src="([^"]*main[^"]*\.js[^"]*)"',
            html
        )

        if not coincidencia:
            print("No se encontró el JavaScript principal.")
            return

        js_url = coincidencia.group(1)

        if js_url.startswith("/"):
            js_url = BASE + js_url
        elif not js_url.startswith("http"):
            js_url = BASE + "/" + js_url

        print("\nArchivo JavaScript:")
        print(js_url)

        js_respuesta = requests.get(
            js_url,
            headers=HEADERS,
            timeout=30
        )
        js_respuesta.raise_for_status()

        js = js_respuesta.text

        print("Tamaño JavaScript:", len(js), "bytes")

        print("\nBUSCANDO INFORMACIÓN EN JAVASCRIPT")

        palabras = [
            "episode",
            "season",
            "tvEpisode",
            "episodeNumber",
            "seasonNumber",
            "graphql",
            "catalog",
            "playback"
        ]

        for palabra in palabras:
            mostrar_coincidencias(js, palabra, limite=3)

        print("\nINVESTIGACIÓN TERMINADA.")

    except Exception as error:
        print("\nERROR:", repr(error))

if __name__ == "__main__":
    main()
