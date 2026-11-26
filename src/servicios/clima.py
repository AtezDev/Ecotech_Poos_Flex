import math

import requests

from dominio.clima import Clima
from persistencia.clima_dao import ClimaDAO
from servicios.api_clima import consultar_api_clima, extraer_clima
from servicios.permisos import exigir_sesion


def validar_coordenadas(latitud, longitud):
    for valor, minimo, maximo, nombre in (
        (latitud, -90, 90, "latitud"),
        (longitud, -180, 180, "longitud"),
    ):
        if type(valor) not in (int, float) or not math.isfinite(valor):
            raise TypeError(f"La {nombre} debe ser numérica.")
        if not minimo <= valor <= maximo:
            raise ValueError(f"La {nombre} está fuera de rango.")
    return float(latitud), float(longitud)


def consultar_clima(usuario, ciudad, latitud, longitud):
    exigir_sesion(usuario)
    ciudad = Clima.validar_ciudad(ciudad)
    latitud, longitud = validar_coordenadas(latitud, longitud)

    try:
        clima = extraer_clima(consultar_api_clima(latitud, longitud), ciudad)
    except (requests.RequestException, ValueError, TypeError):
        return ClimaDAO.ultimo(ciudad), "respaldo"

    ClimaDAO.guardar(clima)
    return clima, "api"
