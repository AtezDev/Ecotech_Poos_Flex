from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.empleado_proyecto_dao import EmpleadoProyectoDAO
from persistencia.proyecto_dao import ProyectoDAO
from presentacion.menu_empleado import solicitar_id_de, tipos_errores_bd


def asignar_a_proyecto():
    id_empleado = solicitar_id_de("empleado")
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if empleado is None or proyecto is None:
            print("El empleado o el proyecto no existe.")
            return
        guardada = EmpleadoProyectoDAO.asignar(empleado, proyecto)
    except IntegrityError:
        print("No se pudo asignar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la asignación.")
    else:
        if guardada:
            print("Empleado asignado al proyecto.")
        else:
            print("El empleado ya estaba asignado a ese proyecto.")


def quitar_de_proyecto():
    id_empleado = solicitar_id_de("empleado")
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if empleado is None or proyecto is None:
            print("El empleado o el proyecto no existe.")
            return
        quitada = EmpleadoProyectoDAO.desasignar(empleado, proyecto)
    except IntegrityError:
        print("No se puede quitar: el empleado tiene registros de tiempo en ese proyecto.")
    except OperationalError:
        print("No se pudo completar la operación.")
    else:
        if quitada:
            print("Empleado quitado del proyecto.")
        else:
            print("Ese empleado no estaba asignado a ese proyecto.")


def proyectos_de_empleado():
    id_empleado = solicitar_id_de("empleado")
    _, OperationalError = tipos_errores_bd()
    try:
        ids = EmpleadoProyectoDAO.listar_por_empleado(id_empleado)
        proyectos = []
        for id_proyecto in ids:
            proyectos.append(ProyectoDAO.buscar_por_id(id_proyecto))
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not proyectos:
            print("Ese empleado no tiene proyectos asignados.")
        for proyecto in proyectos:
            print(proyecto.mostrar_datos())


def empleados_de_proyecto():
    id_proyecto = solicitar_id_de("proyecto")
    _, OperationalError = tipos_errores_bd()
    try:
        ids = EmpleadoProyectoDAO.listar_por_proyecto(id_proyecto)
        empleados = []
        for id_empleado in ids:
            empleados.append(EmpleadoDAO.buscar_por_id(id_empleado))
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not empleados:
            print("Ese proyecto no tiene empleados asignados.")
        for empleado in empleados:
            print(empleado.mostrar_datos())


def asignar_a_departamento():
    id_empleado = solicitar_id_de("empleado")
    id_departamento = solicitar_id_de("departamento")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        if DepartamentoDAO.buscar_por_id(id_departamento) is None:
            print("No existe departamento con ese ID.")
            return
        if id_empleado in DepartamentoDAO.listar_empleados(id_departamento):
            print("El empleado ya pertenece a ese departamento.")
            return
        filas = DepartamentoDAO.asignar_empleado(id_empleado, id_departamento)
    except IntegrityError:
        print("No se pudo asignar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la asignación.")
    else:
        if filas == 1:
            print("Empleado asignado al departamento.")
        else:
            print("No existe un empleado con ese ID.")


def quitar_de_departamento():
    id_empleado = solicitar_id_de("empleado")
    _, OperationalError = tipos_errores_bd()
    try:
        filas = DepartamentoDAO.quitar_empleado(id_empleado)
    except OperationalError:
        print("No se pudo completar la operación.")
    else:
        if filas == 1:
            print("Empleado sin departamento.")
        else:
            print("No existe el empleado o ya no tenía departamento.")


def empleados_de_departamento():
    id_departamento = solicitar_id_de("departamento")
    _, OperationalError = tipos_errores_bd()
    try:
        ids = DepartamentoDAO.listar_empleados(id_departamento)
        empleados = []
        for id_empleado in ids:
            empleados.append(EmpleadoDAO.buscar_por_id(id_empleado))
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not empleados:
            print("Ese departamento no tiene empleados.")
        for empleado in empleados:
            print(empleado.mostrar_datos())


def menu_asignaciones():
    while True:
        print("\n--- ECOTECH: ASIGNACIONES ---")
        print("1. Asignar empleado a proyecto\n2. Quitar empleado de proyecto")
        print("3. Proyectos de un empleado\n4. Empleados de un proyecto")
        print("5. Asignar empleado a departamento\n6. Quitar empleado de departamento")
        print("7. Empleados de un departamento\n0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            asignar_a_proyecto()
        elif opcion == "2":
            quitar_de_proyecto()
        elif opcion == "3":
            proyectos_de_empleado()
        elif opcion == "4":
            empleados_de_proyecto()
        elif opcion == "5":
            asignar_a_departamento()
        elif opcion == "6":
            quitar_de_departamento()
        elif opcion == "7":
            empleados_de_departamento()
        elif opcion == "0":
            break
        else:
            print("Elige una opción entre 0 y 7.")
