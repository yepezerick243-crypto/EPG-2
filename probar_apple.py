
import requests
import re
import json
from bs4 import BeautifulSoup

URL = "https://tv.apple.com/fr/show/two-and-a-half-men/umc.cmc.4syd3ylis0va9bpj1y923v20g?l=en"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9"
}


def convertir_episodio(codigo):
    coincidencia = re.search(r"S(\d+)\s*E(\d+)", codigo, re.I)

    if coincidencia:
        temporada = coincidencia.group(1)
        episodio = coincidencia.group(2)
        return f"Temporada {temporada} Episodio {episodio}"

    return None


def buscar_datos():
    print("=" * 60)
    print("PRUEBA DE APPLE TV")
    print("TWO AND A HALF MEN")
    print("=" * 60)

    try:
        respuesta = requests.get(
            URL,
            headers=HEADERS,
            timeout=30
        )

        print("Estado HTTP:", respuesta.status_code)
        print("Tamaño recibido:", len(respuesta.content), "bytes")

        respuesta.raise_for_status()

        soup = BeautifulSoup(respuesta.text, "html.parser")

        print("\nTÍTULO DE LA PÁGINA:")
        print(
            soup.title.get_text(strip=True)
            if soup.title else "No encontrado"
        )

        print("\nBUSCANDO INFORMACIÓN DE EPISODIOS...")

        encontrados = set()

        # Buscar códigos de episodios en el HTML
        for coincidencia in re.findall(
            r"S\d{1,2}E\d{1,3}",
            respuesta.text,
            re.I
        ):
            formato = convertir_episodio(coincidencia)
            if formato:
                encontrados.add(formato)

        # Buscar nombres y temporadas dentro de los datos JSON
        for script in soup.find_all("script"):
            contenido = script.string or script.get_text()

            for coincidencia in re.findall(
                r"S\d{1,2}E\d{1,3}",
                contenido,
                re.I
            ):
                formato = convertir_episodio(coincidencia)
                if formato:
                    encontrados.add(formato)

        if encontrados:
            print("\nEPISODIOS ENCONTRADOS:")
            for episodio in sorted(
                encontrados,
                key=lambda x: tuple(map(int, re.findall(r"\d+", x)))
            ):
                print(episodio)
        else:
            print("No se encontraron códigos de episodios en el HTML.")

        print("\nPRUEBA TERMINADA.")

    except requests.RequestException as error:
        print("\nERROR DE CONEXIÓN:")
        print(error)

    except Exception as error:
        print("\nERROR:")
        print(repr(error))


if __name__ == "__main__":
    buscar_datos()
