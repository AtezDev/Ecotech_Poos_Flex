import math

from dominio.clima import Clima
from presentacion.menu_empleado import tipos_errores_bd
from servicios.clima import consultar_clima

ORIGENES = {
    "api": "API (dato recién consultado y guardado)",
    "respaldo": "respaldo local (la API no respondió o el dato no es válido)",
}


def solicitar_ciudad():
    while True:
        texto = input("Ciudad (solo letras, por ejemplo La Serena): ")
        try:
            return Clima.validar_ciudad(texto)
        except (TypeError, ValueError) as error:
            print(f"Ciudad no válida: {error}")


def solicitar_numero(mensaje, minimo, maximo):
    while True:
        texto = input(mensaje).strip().replace(",", ".")

        if not texto:
            print("Este dato es obligatorio.")
            continue

        try:
            valor = float(texto)
        except ValueError:
            print("Escribe solo un número, por ejemplo -29.9.")
            continue

        if not math.isfinite(valor):
            print("Escribe un número válido, no infinito ni vacío.")
            continue

        if minimo <= valor <= maximo:
            return valor

        print(f"Debe estar entre {minimo} y {maximo}.")


def menu_clima(usuario_actual):
    _, OperationalError = tipos_errores_bd()

    ciudad = solicitar_ciudad()
    latitud = solicitar_numero("Latitud (-90 a 90): ", -90, 90)
    longitud = solicitar_numero("Longitud (-180 a 180): ", -180, 180)

    try:
        clima, origen = consultar_clima(usuario_actual, ciudad, latitud, longitud)
    except PermissionError as error:
        print(error)
    except (TypeError, ValueError) as error:
        print(f"Datos no válidos: {error}")
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if clima is None:
            print("No hay información de clima disponible para esa ciudad.")
        else:
            print(clima.mostrar_datos())
            print(f"Origen: {ORIGENES[origen]}")
