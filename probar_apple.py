import requests
import re

URL = "https://tv.apple.com/assets/main~Bel1jRMkHC.js"

r = requests.get(URL, headers={"User-Agent": "Mozilla/5.0"}, timeout=40)
r.raise_for_status()
js = r.text

print("=" * 60)
print("DEFINICIONES DE PARÁMETROS APPLE TV")
print("=" * 60)

for nombre, patrones in {
    "Sp": [r"\bSp\s*=", r"\bSp\s*:"],
    "C9": [r"\bC9\s*=", r"\bC9\s*:"],
    "dH": [r"\bdH\s*="],
    "LT": [r"\bLT\s*="],
}.items():

    print(f"\n========== {nombre} ==========")
    posiciones = set()

    for patron in patrones:
        posiciones.update(m.start() for m in re.finditer(patron, js))

    print("Coincidencias:", len(posiciones))

    for posicion in sorted(posiciones)[:5]:
        print("\n--- CONTEXTO ---")
        print(js[max(0, posicion-500):posicion+1000])

print("\nFIN DEL ANÁLISIS")
