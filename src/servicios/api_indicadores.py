import requests

from dominio.indicador import Indicador

URL_INDICADORES = "https://api.boostr.cl/economy/indicators.json"
ESPERA_CONEXION = (3, 5)


def consultar_api():
    respuesta = requests.get(URL_INDICADORES, timeout=ESPERA_CONEXION)
    respuesta.raise_for_status()
    return respuesta.json()


def extraer_primero(datos):
    if not isinstance(datos, dict):
        raise ValueError("Respuesta inesperada de la API.")

    serie = datos.get("serie")

    if not isinstance(serie, list) or not serie or not isinstance(serie[0], dict):
        raise ValueError("La API no entregó una serie de valores.")

    primero = serie[0]
    fecha_publicada = primero.get("fecha")

    if not isinstance(fecha_publicada, str):
        raise ValueError("La API no entregó la fecha del valor.")

    # La fecha es la del dato publicado, no la de hoy: se conservan los 10 primeros caracteres.
    return Indicador(datos.get("codigo"), fecha_publicada[:10], primero.get("valor"))
