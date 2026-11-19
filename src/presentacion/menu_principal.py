from persistencia.semillas import cargar_semillas
from presentacion.menu_asignacion import menu_asignaciones
from presentacion.menu_departamento import menu_departamentos
from presentacion.menu_empleado import menu_empleados, tipos_errores_bd
from presentacion.menu_proyecto import menu_proyectos
from presentacion.menu_registro_tiempo import menu_registros_tiempo


def cargar_datos_de_ejemplo():
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        departamentos, empleados = cargar_semillas()
    except IntegrityError:
        print("No se pudieron cargar las semillas: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la carga de semillas.")
    else:
        if departamentos == 0 and empleados == 0:
            print("Las semillas ya estaban cargadas; no se duplicó ningún dato.")
        else:
            print(f"Semillas cargadas: {departamentos} departamentos y {empleados} empleados nuevos.")


def menu_principal():
    while True:
        print("\n=== ECOTECH SOLUTIONS ===")
        print("1. Empleados\n2. Departamentos\n3. Proyectos")
        print("4. Asignaciones\n5. Registros de tiempo")
        print("6. Cargar datos de ejemplo (semillas)\n0. Salir")
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
        elif opcion == "0":
            print("Saliendo de EcoTech.")
            break
        else:
            print("Elige una opción entre 0 y 6.")
