
import requests
import json

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept-Language": "en-US,en;q=0.9"
}

respuesta = requests.get(URL, headers=HEADERS, timeout=30)
respuesta.raise_for_status()

html = respuesta.text

print("=" * 65)
print("IDENTIFICADORES DE TEMPORADAS - APPLE TV")
print("=" * 65)

posicion = html.find('"seasons":')

if posicion == -1:
    print("No se encontró la lista de temporadas.")
else:
    inicio = html.find("[", posicion)

    try:
        temporadas, fin = json.JSONDecoder().raw_decode(
            html[inicio:]
        )

        print("Temporadas encontradas:", len(temporadas))

        for temporada in temporadas:
            print(
                f"Temporada {temporada.get('seasonNumber')}: "
                f"{temporada.get('id')} | "
                f"Episodios: {temporada.get('episodeCount')}"
            )

    except Exception as error:
        print("Error leyendo temporadas:", error)

print("\n" + "=" * 65)
print("CONFIGURACIÓN DE LA API DE EPISODIOS")
print("=" * 65)

for palabra in ['"contentEpisodes"', '"getSeasonDetailById"']:
    posicion = html.find(palabra)

    print("\n", palabra)

    if posicion == -1:
        print("No encontrado en el HTML.")
    else:
        print(html[posicion:posicion + 700])

print("\nDIAGNÓSTICO TERMINADO")
