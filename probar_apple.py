
import requests
import re

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

print("=" * 65)
print("ANÁLISIS DE SOLICITUDES API V3")
print("=" * 65)

respuesta = requests.get(
    URL,
    headers=HEADERS,
    timeout=40
)
respuesta.raise_for_status()

html = respuesta.text

# Buscar archivos JavaScript utilizados por Apple TV
scripts = re.findall(
    r'<script[^>]+src=["\']([^"\']+\.js[^"\']*)',
    html
)

print("\nArchivos JavaScript encontrados:", len(scripts))

for script_url in scripts:
    if script_url.startswith("/"):
        script_url = "https://tv.apple.com" + script_url
    elif script_url.startswith("//"):
        script_url = "https:" + script_url

    if "main~" not in script_url:
        continue

    print("\nDescargando:", script_url)

    js = requests.get(
        script_url,
        headers=HEADERS,
        timeout=40
    ).text

    print("Tamaño:", len(js))

    patrones = [
        "getSeasonDetailById",
        "getSeasonMetadataById",
        "contentEpisodes",
        "caller=web",
        "caller",
        "utsk",
        "X-Apple-Store-Front",
        "seasonId"
    ]

    for patron in patrones:
        posiciones = [
            m.start()
            for m in re.finditer(
                re.escape(patron),
                js,
                re.IGNORECASE
            )
        ]

        print(f"\n{patron}: {len(posiciones)} coincidencias")

        for posicion in posiciones[:2]:
            inicio = max(0, posicion - 700)
            fin = min(len(js), posicion + 1300)

            print(js[inicio:fin])
            print("\n" + "-" * 50)

    break

print("\nANÁLISIS TERMINADO")
