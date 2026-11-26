from presentacion.menu_empleado import tipos_errores_bd
from presentacion.menu_clima import menu_clima
from servicios.indicadores import actualizar_uf, consultar_uf_guardada

ORIGENES = {
    "api": "API (dato recién consultado y guardado)",
    "respaldo": "respaldo local (la API no respondió)",
}


def mostrar_indicador(indicador, origen=None):
    if indicador is None:
        print("No hay información disponible para la UF.")
        return

    print(indicador.mostrar_datos())

    if origen is not None:
        print(f"Origen: {ORIGENES[origen]}")


def menu_indicadores(usuario_actual):
    _, OperationalError = tipos_errores_bd()

    while True:
        print("\n=== INDICADORES ECONÓMICOS ===")
        print("1. Consultar UF guardada")
        print("2. Actualizar UF desde la API (solo administrador)")
        print("3. Consultar clima (API de Open-Meteo)")
        print("0. Volver")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            try:
                indicador = consultar_uf_guardada(usuario_actual)
            except PermissionError as error:
                print(error)
            except OperationalError:
                print("No se pudo consultar la base de datos.")
            else:
                mostrar_indicador(indicador)

        elif opcion == "2":
            try:
                indicador, origen = actualizar_uf(usuario_actual)
            except PermissionError as error:
                print(error)
            except OperationalError:
                print("No se pudo completar la operación en la BD.")
            else:
                mostrar_indicador(indicador, origen)

        elif opcion == "3":
            menu_clima(usuario_actual)

        elif opcion == "0":
            break

        else:
            print("Opción inválida.")
