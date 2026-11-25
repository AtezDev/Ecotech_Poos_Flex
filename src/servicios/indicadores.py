import requests

from persistencia.indicador_dao import IndicadorDAO
from servicios.api_indicadores import consultar_api, extraer_primero
from servicios.permisos import exigir_admin, exigir_sesion


def actualizar_uf(usuario):
    exigir_admin(usuario)

    try:
        indicador = extraer_primero(consultar_api())
    except (requests.RequestException, ValueError, TypeError):
        # Si la API falla, mostramos el último dato guardado en EcoTech.
        return IndicadorDAO.ultimo("UF"), "respaldo"

    IndicadorDAO.guardar(indicador)
    return indicador, "api"


def consultar_uf_guardada(usuario):
    exigir_sesion(usuario)
    return IndicadorDAO.ultimo("UF")
