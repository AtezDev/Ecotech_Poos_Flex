from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from presentacion.menu_comun import (eliminar_con_confirmacion, buscar_uno, listar_todo,
                                     validar_texto_obligatorio)
from presentacion.menu_empleado import solicitar, solicitar_id_de, tipos_errores_bd


def seleccionar_gerente():
    empleados = EmpleadoDAO.listar()
    if not empleados:
        print("Todavía no hay empleados registrados: el departamento quedará sin gerente.")
        print("Cuando registres empleados, asigna el gerente con la opción 5.")
        return None
    print("El gerente es un empleado ya registrado. Empleados disponibles:")
    for empleado in empleados:
        print(f"  {empleado.id}: {empleado.nombre}")
    while True:
        texto = input("ID del gerente (Enter para dejarlo sin gerente): ").strip()
        if texto == "":
            return None
        try:
            id_gerente = int(texto)
        except ValueError:
            print("Escribe solo el número de ID del empleado.")
            continue
        if id_gerente <= 0:
            print("El ID debe ser positivo.")
            continue
        gerente = EmpleadoDAO.buscar_por_id(id_gerente)
        if gerente is None:
            print("No existe ningún empleado con ese ID. Elige uno de la lista.")
        else:
            return gerente


def crear_departamento():
    nombre = solicitar("Nombre", validar_texto_obligatorio)
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        if DepartamentoDAO.buscar_id_por_nombre(nombre) is not None:
            print("Ya existe un departamento con ese nombre; no se registró de nuevo.")
            return
        gerente = seleccionar_gerente()
        departamento = Departamento(nombre, gerente)
        DepartamentoDAO.insertar(departamento)
    except IntegrityError:
        print("No se pudo registrar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo conectar o completar el registro.")
    else:
        print(f"Departamento registrado. ID: {departamento.id}")


def listar_departamentos():
    listar_todo(DepartamentoDAO.listar, "Todavía no hay departamentos registrados.")


def buscar_departamento():
    buscar_uno("departamento", DepartamentoDAO.buscar_por_id)


def actualizar_nombre_departamento():
    id_departamento = solicitar_id_de("departamento")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        if departamento is None:
            print("No existe departamento con ese ID.")
            return
        nuevo = solicitar("Nombre", validar_texto_obligatorio)
        if nuevo == departamento.obtenerNombre():
            print("El valor es el mismo; no hay cambios.")
            return
        departamento.cambiarNombre(nuevo)
        filas = DepartamentoDAO.actualizar(departamento)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Nombre actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_gerente_departamento():
    id_departamento = solicitar_id_de("departamento")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)
        if departamento is None:
            print("No existe departamento con ese ID.")
            return
        nuevo = seleccionar_gerente()
        id_actual = departamento.gerente.id if departamento.gerente is not None else None
        id_nuevo = nuevo.id if nuevo is not None else None
        if id_nuevo == id_actual:
            print("El valor es el mismo; no hay cambios.")
            return
        departamento.cambiarGerente(nuevo)
        filas = DepartamentoDAO.actualizar(departamento)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Gerente actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def eliminar_departamento():
    eliminar_con_confirmacion("departamento", DepartamentoDAO.buscar_por_id,
                              DepartamentoDAO.eliminar)


def menu_departamentos():
    while True:
        print("\n--- ECOTECH: DEPARTAMENTOS ---")
        print("1. Registrar\n2. Listar\n3. Buscar por ID")
        print("4. Actualizar nombre\n5. Actualizar gerente\n6. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_departamento()
        elif opcion == "2":
            listar_departamentos()
        elif opcion == "3":
            buscar_departamento()
        elif opcion == "4":
            actualizar_nombre_departamento()
        elif opcion == "5":
            actualizar_gerente_departamento()
        elif opcion == "6":
            eliminar_departamento()
        elif opcion == "0":
            break
        else:
            print("Elige una opción entre 0 y 6.")
