from presentacion.menu_clima import menu_clima
from presentacion.menu_empleado import tipos_errores_bd
from servicios.indicadores import (
    actualizar_indicadores,
    consultar_indicador_guardado,
)

ORIGENES = {
    "api": "API (dato recién consultado y guardado)",
    "respaldo": "respaldo local (la API no respondió)",
}


def mostrar_indicador(indicador, origen=None, codigo=None):
    if indicador is None:
        print(f"No hay información disponible para {codigo or 'este indicador'}.")
        return

    print(indicador.mostrar_datos())

    if origen is not None:
        print(f"Origen: {ORIGENES[origen]}")


def menu_indicadores(usuario_actual):
    _, OperationalError = tipos_errores_bd()

    while True:
        print("\n=== INDICADORES ECONÓMICOS ===")
        print("1. Consultar indicador guardado (UF, DOLAR o EURO)")
        print("2. Actualizar indicadores desde la API (solo administrador)")
        print("3. Consultar clima (API de Open-Meteo)")
        print("0. Volver")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            codigo = input("Indicador (UF, DOLAR o EURO): ").strip().upper()
            try:
                indicador = consultar_indicador_guardado(usuario_actual, codigo)
            except (PermissionError, ValueError) as error:
                print(error)
            except OperationalError:
                print("No se pudo consultar la base de datos.")
            else:
                mostrar_indicador(indicador, codigo=codigo)

        elif opcion == "2":
            try:
                indicadores, origen = actualizar_indicadores(usuario_actual)
            except PermissionError as error:
                print(error)
            except OperationalError:
                print("No se pudo completar la operación en la BD.")
            else:
                for indicador, codigo in zip(indicadores, ("UF", "DOLAR", "EURO")):
                    mostrar_indicador(indicador, origen, codigo)

        elif opcion == "3":
            menu_clima(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")
