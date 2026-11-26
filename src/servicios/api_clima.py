import requests

from dominio.clima import Clima
from servicios.api_indicadores import validar_respuesta_http

URL_CLIMA = "https://api.open-meteo.com/v1/forecast"
ESPERA_CONEXION = (3, 5)


def consultar_api_clima(latitud, longitud):
    parametros = {
        "latitude": latitud,
        "longitude": longitud,
        "current": "temperature_2m,relative_humidity_2m,weather_code",
    }
    respuesta = requests.get(URL_CLIMA, params=parametros, timeout=ESPERA_CONEXION)
    validar_respuesta_http(respuesta)
    return respuesta.json()


def extraer_clima(datos, ciudad):
    if not isinstance(datos, dict) or not isinstance(datos.get("current"), dict):
        raise ValueError("La API no entregó datos de clima.")

    actual = datos["current"]
    codigo = actual.get("weather_code")

    if type(codigo) is not int:
        raise ValueError("La API no entregó el estado del clima.")

    return Clima(
        ciudad,
        actual.get("time"),
        actual.get("temperature_2m"),
        actual.get("relative_humidity_2m"),
        Clima.traducir_estado(codigo),
    )
