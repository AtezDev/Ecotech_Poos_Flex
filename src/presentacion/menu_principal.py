
from dominio.empleado import Empleado
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.semillas import cargar_semillas
from presentacion.menu_indicadores import menu_indicadores
from presentacion.menu_asignacion import menu_asignaciones
from presentacion.menu_departamento import menu_departamentos
from presentacion.menu_empleado import menu_empleados, solicitar, tipos_errores_bd
from presentacion.menu_proyecto import menu_proyectos
from presentacion.menu_registro_tiempo import menu_registros_tiempo


def cargar_datos_de_ejemplo():
    IntegrityError, OperationalError = tipos_errores_bd()

    try:
        departamentos, empleados = cargar_semillas()

    except IntegrityError:
        print(
            "No se pudieron cargar las semillas: "
            "revisa las restricciones de la BD."
        )

    except OperationalError:
        print("No se pudo completar la carga de semillas.")

    except (TypeError, ValueError) as error:
        print(f"No se pudieron cargar las semillas: {error}")

    else:
        if departamentos == 0 and empleados == 0:
            print(
                "Las semillas ya estaban cargadas; "
                "no se duplicó ningún dato."
            )
        else:
            print(
                f"Semillas cargadas: {departamentos} departamentos "
                f"y {empleados} empleados nuevos."
            )


def mostrar_mi_ficha(usuario_actual):
    _, OperationalError = tipos_errores_bd()

    try:
        empleado = EmpleadoDAO.buscar_por_id(usuario_actual.empleado_id)
    except OperationalError:
        print("No se pudo consultar la base de datos.")
        return

    if empleado is None:
        print("No se encontró tu ficha de empleado.")
    else:
        print(empleado.mostrar_datos())


def modificar_mis_datos(usuario_actual):
    IntegrityError, OperationalError = tipos_errores_bd()

    while True:
        print("\n=== MODIFICAR MIS DATOS ===")
        print("1. Dirección")
        print("2. Teléfono")
        print("3. Correo electrónico")
        print("0. Volver")

        opcion = input("Opción: ").strip()

        if opcion == "0":
            return
        if opcion not in ("1", "2", "3"):
            print("Elige una opción entre 0 y 3.")
            continue

        try:
            empleado = EmpleadoDAO.buscar_por_id(usuario_actual.empleado_id)
        except OperationalError:
            print("No se pudo consultar la base de datos.")
            continue

        if empleado is None:
            print("No se encontró tu ficha de empleado.")
            return

        try:
            if opcion == "1":
                nuevo = solicitar("Dirección", Empleado.validar_direccion)
                if nuevo == empleado.obtenerDireccion():
                    print("El valor es el mismo; no hay cambios.")
                    continue
                empleado.cambiarDireccion(nuevo)
            elif opcion == "2":
                nuevo = solicitar("Teléfono", Empleado.validar_telefono)
                if nuevo == empleado.obtenerTelefono():
                    print("El valor es el mismo; no hay cambios.")
                    continue
                empleado.cambiarTelefono(nuevo)
            else:
                nuevo = solicitar("Correo electrónico", Empleado.validar_correo)
                if nuevo == empleado.obtenerCorreoElectronico():
                    print("El valor es el mismo; no hay cambios.")
                    continue
                existente = EmpleadoDAO.buscar_id_por_correo(nuevo)
                if existente is not None and existente != empleado.id:
                    print("Ese correo ya está registrado en otra ficha.")
                    continue
                empleado.cambiarCorreoElectronico(nuevo)
            filas = EmpleadoDAO.actualizar(empleado)
        except IntegrityError:
            print("No se pudo actualizar: el correo ya está registrado en otra ficha.")
        except OperationalError:
            print("No se pudo completar la actualización.")
        else:
            if filas == 1:
                print("Dato actualizado correctamente.")
            else:
                print("No hubo cambios en la BD; consulta con el administrador.")


def menu_empleado_sesion(usuario_actual):
    from presentacion.menu_usuario import menu_mi_cuenta

    while True:
        print("\n=== ECOTECH SOLUTIONS ===")
        print("1. Mi ficha")
        print("2. Modificar mis datos")
        print("3. Indicadores económicos")
        print("4. Mi cuenta")
        print("0. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            mostrar_mi_ficha(usuario_actual)

        elif opcion == "2":
            modificar_mis_datos(usuario_actual)

        elif opcion == "3":
            menu_indicadores(usuario_actual)

        elif opcion == "4":
            if menu_mi_cuenta(usuario_actual):
                print("Saliendo de EcoTech.")
                return True

        elif opcion == "0":
            print("Saliendo de EcoTech.")
            break

        else:
            print("Opción inválida.")


def menu_principal(usuario_actual=None):
    if usuario_actual is not None and not usuario_actual.es_admin:
        return menu_empleado_sesion(usuario_actual)

    while True:
        print("\n=== ECOTECH SOLUTIONS ===")
        print("1. Empleados")
        print("2. Departamentos")
        print("3. Proyectos")
        print("4. Asignaciones")
        print("5. Registros de tiempo")
        print("6. Cargar datos de ejemplo (semillas)")

        if usuario_actual is not None:
            print("7. Mi cuenta")
            print("8. Administrar usuarios")
            print("9. Indicadores económicos")

        print("0. Salir")

        opcion = input("Opción: ").strip()

        if opcion == "1":
            menu_empleados()

        elif opcion == "2":
            menu_departamentos()

        elif opcion == "3":
            menu_proyectos()

        elif opcion == "4":
            menu_asignaciones()

        elif opcion == "5":
            menu_registros_tiempo()

        elif opcion == "6":
            cargar_datos_de_ejemplo()

        elif opcion == "7":
            if usuario_actual is None:
                print("Opción no disponible.")
            else:
                from presentacion.menu_usuario import menu_mi_cuenta

                if menu_mi_cuenta(usuario_actual):
                    print("Saliendo de EcoTech.")
                    return True

        elif opcion == "8":
            if usuario_actual is not None:
                from presentacion.menu_usuario import (
                    menu_administrar_usuarios
                )

                menu_administrar_usuarios(usuario_actual)
            else:
                print("Opción no disponible.")

        elif opcion == "9":
            if usuario_actual is None:
                print("Opción no disponible.")
            else:
                menu_indicadores(usuario_actual)

        elif opcion == "0":
            print("Saliendo de EcoTech.")
            break

        else:
            print("Opción inválida.")
