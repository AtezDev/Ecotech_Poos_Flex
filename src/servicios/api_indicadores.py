import requests

from dominio.indicador import Indicador

URL_INDICADORES = "https://api.boostr.cl/economy/indicators.json"
ESPERA_CONEXION = (3, 5)
CLAVES_API = {"uf": "UF", "dolar": "DOLAR", "euro": "EURO"}


def consultar_api():
    respuesta = requests.get(URL_INDICADORES, timeout=ESPERA_CONEXION)
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_indicadores(datos):
    if not isinstance(datos, dict) or datos.get("status") != "success":
        raise ValueError("La API no respondió con éxito.")

    contenido = datos.get("data")

    if not isinstance(contenido, dict):
        raise ValueError("La API no entregó datos.")

    indicadores = []

    for clave, codigo in CLAVES_API.items():
        bloque = contenido.get(clave)

        if not isinstance(bloque, dict):
            raise ValueError(f"La API no entregó {codigo}.")

        indicadores.append(Indicador(codigo, bloque.get("date"), bloque.get("value")))

    return indicadores


def extraer_primero(datos):
    for indicador in extraer_indicadores(datos):
        if indicador.codigo == "UF":
            return indicador
    raise ValueError("La API no entregó UF.")
