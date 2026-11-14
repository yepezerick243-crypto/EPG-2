
import requests
import re

URL = "https://tv.apple.com/assets/CommerceModalContainer~DzQAEzo7fs.js"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
r.raise_for_status()
js = r.text

print("=" * 65)
print("INVESTIGACIÓN DEL TOKEN DE APPLE TV")
print("=" * 65)
print("Tamaño del archivo:", len(js))

patrones = [
    r"\bSp\s*=",
    r"\bSp\s*:",
    r"developerToken",
    r"media-user-token",
    r"uts/v3/configurations"
]

for patron in patrones:
    posiciones = [m.start() for m in re.finditer(patron, js, re.I)]
    print(f"\n\nPATRÓN: {patron}")
    print("Coincidencias:", len(posiciones))

    for pos in posiciones[:5]:
        inicio = max(0, pos - 700)
        fin = min(len(js), pos + 1300)
        print("\n--- CONTEXTO ---")
        print(js[inicio:fin])

print("\n" + "=" * 65)
print("FIN DEL ANÁLISIS")
print("=" * 65)
