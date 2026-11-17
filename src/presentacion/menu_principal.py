from presentacion.menu_asignacion import menu_asignaciones
from presentacion.menu_departamento import menu_departamentos
from presentacion.menu_empleado import menu_empleados
from presentacion.menu_proyecto import menu_proyectos
from presentacion.menu_registro_tiempo import menu_registros_tiempo


def menu_principal():
    while True:
        print("\n=== ECOTECH SOLUTIONS ===")
        print("1. Empleados\n2. Departamentos\n3. Proyectos")
        print("4. Asignaciones\n5. Registros de tiempo\n0. Salir")
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
        elif opcion == "0":
            print("Saliendo de EcoTech.")
            break
        else:
            print("Elige una opción entre 0 y 5.")
