
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
print("ANÁLISIS DE CONFIGURACIÓN APPLE TV")
print("=" * 65)

patrones = [
    r"\bSp\s*=",
    r"\bSi\s*=",
    r"function\s+Si\s*\(",
    r"const\s+Si\s*=",
    r"let\s+Si\s*=",
    r"requiredParamsMap",
    r"configurations",
    r"developerToken"
]

for patron in patrones:
    coincidencias = list(
        re.finditer(patron, js)
    )

    print(f"\n{patron}: {len(coincidencias)} coincidencias")

    for coincidencia in coincidencias[:3]:
        inicio = max(0, coincidencia.start() - 500)
        fin = min(len(js), coincidencia.start() + 1800)

        print(js[inicio:fin])
        print("\n" + "-" * 60)

print("\nANÁLISIS TERMINADO")
