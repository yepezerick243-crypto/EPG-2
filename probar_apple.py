
import requests
from bs4 import BeautifulSoup
import re

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

respuesta = requests.get(URL, headers=HEADERS, timeout=30)
respuesta.raise_for_status()

html = respuesta.text
soup = BeautifulSoup(html, "html.parser")

print("=" * 65)
print("DIAGNÓSTICO DE TEMPORADAS - APPLE TV")
print("=" * 65)

print("\n1. SELECTORES DE TEMPORADA")

selectores = soup.find_all("select")

print("Selectores encontrados:", len(selectores))

for i, selector in enumerate(selectores, 1):
    print(f"\nSELECTOR {i}")
    print(selector.prettify()[:5000])

print("\n2. ENLACES RELACIONADOS CON TEMPORADAS")

for enlace in soup.find_all("a", href=True):
    href = enlace["href"]
    texto = enlace.get_text(" ", strip=True)

    if "season" in href.lower() or "temporada" in texto.lower():
        print("Texto:", texto)
        print("Enlace:", href)

print("\n3. DATOS INTERNOS DE TEMPORADAS")

patrones = [
    "SeasonPageIntent",
    "BoxSetEpisodesPaginationIntent",
    "seasonNumber",
    "seasonId",
    "season"
]

for patron in patrones:
    posiciones = [
        m.start() for m in re.finditer(
            re.escape(patron), html, re.IGNORECASE
        )
    ]

    print(f"\n{patron}: {len(posiciones)} coincidencias")

    for posicion in posiciones[:3]:
        inicio = max(0, posicion - 350)
        fin = min(len(html), posicion + 700)
        print(html[inicio:fin])
        print("-" * 40)

print("\nDIAGNÓSTICO TERMINADO")
