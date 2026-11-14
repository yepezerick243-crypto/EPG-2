
import requests
import re

URL = "https://tv.apple.com/assets/main~Bel1jRMkHC.js"

r = requests.get(
    URL,
    headers={"User-Agent": "Mozilla/5.0"},
    timeout=40
)
r.raise_for_status()
js = r.text

print("=" * 65)
print("DEFINICIONES DE PARÁMETROS APPLE TV")
print("=" * 65)

for nombre in ["Sp", "C9", "dH", "LT"]:
    print(f"\n\n========== {nombre} ==========")

    if nombre == "Sp":
        patrones = [
            r"\bSp\s*=",
            r"\bSp\s*:",
            r"\bSp\b"
        ]
    elif nombre == "C9":
        patrones = [
            r"\bC9\s*=",
            r"\bC9\s*:"
        ]
    elif nombre == "dH":
        patrones = [
            r"\bdH\s*="
        ]
    else:
        patrones = [
            r"\bLT\s*="
        ]

    posiciones = set()

    for patron in patrones:
        for m in re.finditer(patron, js):
            posiciones.add(m.start())

    print("Coincidencias:", len(posiciones))

    for posicion in sorted(posiciones)[:8]:
        inicio = max(0, posicion - 900)
        fin = min(len(js), posicion + 1800)

        print("\n--- CONTEXTO ---")
        print(js[inicio:fin])

print("\n" + "=" * 65)
print("FIN DEL ANÁLISIS")
print("=" * 65)
