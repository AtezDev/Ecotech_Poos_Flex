from dominio.proyecto import Proyecto
from persistencia.proyecto_dao import ProyectoDAO
from presentacion.menu_comun import (eliminar_con_confirmacion, buscar_uno, listar_todo,
                                     validar_texto_obligatorio)
from presentacion.menu_empleado import (solicitar, solicitar_fecha, solicitar_id_de,
                                        tipos_errores_bd)


def crear_proyecto():
    nombre = solicitar("Nombre", validar_texto_obligatorio)
    descripcion = solicitar("Descripción", validar_texto_obligatorio)
    fecha = solicitar("Fecha de inicio (AAAA-MM-DD)", solicitar_fecha)
    proyecto = Proyecto(nombre, descripcion, fecha)
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        ProyectoDAO.insertar(proyecto)
    except IntegrityError:
        print("No se pudo registrar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo conectar o completar el registro.")
    else:
        print(f"Proyecto registrado. ID: {proyecto.id}")


def listar_proyectos():
    listar_todo(ProyectoDAO.listar, "Todavía no hay proyectos registrados.")


def buscar_proyecto():
    buscar_uno("proyecto", ProyectoDAO.buscar_por_id)


def actualizar_nombre_proyecto():
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if proyecto is None:
            print("No existe proyecto con ese ID.")
            return
        nuevo = solicitar("Nombre", validar_texto_obligatorio)
        if nuevo == proyecto.obtenerNombre():
            print("El valor es el mismo; no hay cambios.")
            return
        proyecto.cambiarNombre(nuevo)
        filas = ProyectoDAO.actualizar(proyecto)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Nombre actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_descripcion_proyecto():
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if proyecto is None:
            print("No existe proyecto con ese ID.")
            return
        nuevo = solicitar("Descripción", validar_texto_obligatorio)
        if nuevo == proyecto.obtenerDescripcion():
            print("El valor es el mismo; no hay cambios.")
            return
        proyecto.cambiarDescripcion(nuevo)
        filas = ProyectoDAO.actualizar(proyecto)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Descripción actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_fecha_proyecto():
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if proyecto is None:
            print("No existe proyecto con ese ID.")
            return
        nuevo = solicitar("Fecha de inicio (AAAA-MM-DD)", solicitar_fecha)
        if nuevo == proyecto.obtenerFechaInicio():
            print("El valor es el mismo; no hay cambios.")
            return
        proyecto.cambiarFechaInicio(nuevo)
        filas = ProyectoDAO.actualizar(proyecto)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Fecha de inicio (AAAA-MM-DD) actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def eliminar_proyecto():
    eliminar_con_confirmacion("proyecto", ProyectoDAO.buscar_por_id, ProyectoDAO.eliminar)


def menu_proyectos():
    while True:
        print("\n--- ECOTECH: PROYECTOS ---")
        print("1. Registrar\n2. Listar\n3. Buscar por ID")
        print("4. Actualizar nombre\n5. Actualizar descripción")
        print("6. Actualizar fecha de inicio\n7. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_proyecto()
        elif opcion == "2":
            listar_proyectos()
        elif opcion == "3":
            buscar_proyecto()
        elif opcion == "4":
            actualizar_nombre_proyecto()
        elif opcion == "5":
            actualizar_descripcion_proyecto()
        elif opcion == "6":
            actualizar_fecha_proyecto()
        elif opcion == "7":
            eliminar_proyecto()
        elif opcion == "0":
            break
        else:
            print("Elige una opción entre 0 y 7.")
