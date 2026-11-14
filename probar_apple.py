
import requests
import re

URL = "https://tv.apple.com/assets/main~Bel1jRMkHC.js"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
r.raise_for_status()
js = r.text

print("=" * 65)
print("INVESTIGACIÓN DE SOLICITUDES UTS")
print("=" * 65)

patrones = [
    "getShowEpisodes",
    "getSeasonDetailById",
    "getShowDetailById",
    "contentEpisodes",
    "requiredParamsMap",
    "setCommonParams",
    "createApiRequest",
    "getTokenHeaders"
]

for patron in patrones:
    posiciones = [m.start() for m in re.finditer(re.escape(patron), js)]
    print(f"\n\n========== {patron} ==========")
    print("Coincidencias:", len(posiciones))

    for pos in posiciones[:3]:
        inicio = max(0, pos - 1200)
        fin = min(len(js), pos + 2200)
        print("\n--- CONTEXTO ---")
        print(js[inicio:fin])

print("\n" + "=" * 65)
print("FIN DEL ANÁLISIS")
print("=" * 65)
