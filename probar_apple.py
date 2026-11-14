import requests
import re

url = "https://tv.apple.com/assets/main~Bel1jRMkHC.js"
js = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=40).text

print("BUSCANDO EL TOKEN DE APPLE TV")
print("=" * 55)

for termino in ["Sp", "developerToken", "Authorization"]:
    posiciones = [m.start() for m in re.finditer(re.escape(termino), js)]

    print(f"\n{termino}: {len(posiciones)} coincidencias")

    for p in posiciones[:8]:
        print("\n--- CONTEXTO ---")
        print(js[max(0, p-250):p+450])

print("\nFIN")
