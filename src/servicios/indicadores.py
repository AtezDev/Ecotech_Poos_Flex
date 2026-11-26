import requests

from dominio.indicador import Indicador
from persistencia.indicador_dao import IndicadorDAO
from servicios.api_indicadores import consultar_api, extraer_indicadores
from servicios.permisos import exigir_admin, exigir_sesion


def actualizar_indicadores(usuario):
    exigir_admin(usuario)

    try:
        indicadores = extraer_indicadores(consultar_api())
    except (requests.RequestException, ValueError, TypeError):
        # Si la API falla, mostramos el último dato guardado de cada indicador.
        respaldo = [IndicadorDAO.ultimo(codigo) for codigo in Indicador.CODIGOS_VALIDOS]
        return respaldo, "respaldo"

    for indicador in indicadores:
        IndicadorDAO.guardar(indicador)

    return indicadores, "api"


def actualizar_uf(usuario):
    indicadores, origen = actualizar_indicadores(usuario)
    for indicador in indicadores:
        if indicador is not None and indicador.codigo == "UF":
            return indicador, origen
    return None, origen


def consultar_indicador_guardado(usuario, codigo):
    exigir_sesion(usuario)
    if codigo not in Indicador.CODIGOS_VALIDOS:
        raise ValueError("Indicador no reconocido.")
    return IndicadorDAO.ultimo(codigo)


def consultar_uf_guardada(usuario):
    return consultar_indicador_guardado(usuario, "UF")
