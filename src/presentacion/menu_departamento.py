from dominio.departamento import Departamento
from persistencia.departamento_dao import DepartamentoDAO
from presentacion.menu_comun import (eliminar_con_confirmacion, buscar_uno, listar_todo,
                                     validar_texto_obligatorio)
from presentacion.menu_empleado import solicitar, solicitar_id_de, tipos_errores_bd


def crear_departamento():
    nombre = solicitar("Nombre", validar_texto_obligatorio)
    gerente = solicitar("Gerente", validar_texto_obligatorio)
    departamento = Departamento(nombre, gerente)
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
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
        nuevo = solicitar("Gerente", validar_texto_obligatorio)
        if nuevo == departamento.obtenerGerente():
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
