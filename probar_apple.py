
import requests
import json

SHOW_ID = "umc.cmc.4syd3ylis0va9bpj1y923v20g"

SEASON_ID = "umc.cmc.3oy3zhi4rvr8zqu2jwcyli4up"

HEADERS = {
    "User-Agent": "Mozilla/5.0",
    "Accept": "application/json",
    "Accept-Language": "en-US,en;q=0.9",
    "Origin": "https://tv.apple.com",
    "Referer": "https://tv.apple.com/"
}

PARAMS = {
    "l": "en",
    "sf": "143442",
    "locale": "en-US"
}

BASE = "https://uts-api.itunes.apple.com"

PRUEBAS = {
    "EPISODIOS V2": (
        f"{BASE}/uts/v2/content/{SEASON_ID}/episodes"
    ),
    "DETALLE TEMPORADA V3": (
        f"{BASE}/uts/v3/shows/{SHOW_ID}/{SEASON_ID}"
    )
}

sesion = requests.Session()
sesion.headers.update(HEADERS)

print("=" * 65)
print("PRUEBA DE API - APPLE TV")
print("=" * 65)

for nombre, url in PRUEBAS.items():
    print(f"\n\n{'=' * 65}")
    print(nombre)
    print("=" * 65)

    try:
        respuesta = sesion.get(
            url,
            params=PARAMS,
            timeout=40
        )

        print("URL:", respuesta.url)
        print("HTTP:", respuesta.status_code)
        print("Tipo:", respuesta.headers.get("Content-Type"))

        if respuesta.status_code == 200:
            try:
                datos = respuesta.json()

                nombre_archivo = (
                    "respuesta_episodios.json"
                    if "EPISODIOS" in nombre
                    else "respuesta_temporada.json"
                )

                with open(
                    nombre_archivo,
                    "w",
                    encoding="utf-8"
                ) as archivo:
                    json.dump(
                        datos,
                        archivo,
                        ensure_ascii=False,
                        indent=2
                    )

                print("JSON recibido correctamente.")
                print("Archivo guardado:", nombre_archivo)

                if isinstance(datos, dict):
                    print("Claves principales:")
                    print(list(datos.keys()))

                print("\nPrimeros 5000 caracteres:")
                print(
                    json.dumps(
                        datos,
                        ensure_ascii=False,
                        indent=2
                    )[:5000]
                )

            except ValueError:
                print("La respuesta no es JSON:")
                print(respuesta.text[:2000])

        else:
            print("Respuesta del servidor:")
            print(respuesta.text[:2000])

    except Exception as error:
        print("ERROR:", error)

print("\n" + "=" * 65)
print("PRUEBAS TERMINADAS")
print("=" * 65)
