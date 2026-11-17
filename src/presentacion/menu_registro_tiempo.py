from dominio.registro_tiempo import RegistroTiempo
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO
from persistencia.registro_tiempo_dao import RegistroTiempoDAO
from presentacion.menu_comun import (eliminar_con_confirmacion, validar_horas,
                                     validar_texto_obligatorio)
from presentacion.menu_empleado import (solicitar, solicitar_fecha,
                                        solicitar_id_de, tipos_errores_bd)


def describir(registro):
    return (f"{registro.mostrar_datos()} | Empleado: {registro.empleado.id} "
            f"| Proyecto: {registro.proyecto.id}")


def crear_registro():
    id_empleado = solicitar_id_de("empleado")
    id_proyecto = solicitar_id_de("proyecto")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        if empleado is None or proyecto is None:
            print("El empleado o el proyecto no existe.")
            return
        fecha = solicitar("Fecha (AAAA-MM-DD)", solicitar_fecha)
        horas = solicitar("Horas", validar_horas)
        tarea = solicitar("Tarea", validar_texto_obligatorio)
        registro = RegistroTiempo(fecha, horas, tarea)
        registro.registrarTiempo(fecha, horas, tarea, empleado, proyecto)
        RegistroTiempoDAO.insertar(registro)
    except ValueError as error:
        print(f"No se pudo registrar: {error}")
    except IntegrityError:
        print("No se pudo registrar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo conectar o completar el registro.")
    else:
        print(f"Registro de tiempo guardado. ID: {registro.id}")


def listar_registros():
    _, OperationalError = tipos_errores_bd()
    try:
        registros = RegistroTiempoDAO.listar()
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if not registros:
            print("Todavía no hay registros de tiempo.")
        for registro in registros:
            print(describir(registro))


def buscar_registro():
    id_registro = solicitar_id_de("registro de tiempo")
    _, OperationalError = tipos_errores_bd()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
    except OperationalError:
        print("No se pudo consultar la base de datos.")
    else:
        if registro is None:
            print("No existe registro de tiempo con ese ID.")
        else:
            print(describir(registro))


def actualizar_fecha_registro():
    id_registro = solicitar_id_de("registro de tiempo")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if registro is None:
            print("No existe registro de tiempo con ese ID.")
            return
        nuevo = solicitar("Fecha (AAAA-MM-DD)", solicitar_fecha)
        if nuevo == registro.obtenerFecha():
            print("El valor es el mismo; no hay cambios.")
            return
        registro.cambiarFecha(nuevo)
        filas = RegistroTiempoDAO.actualizar(registro)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Fecha (AAAA-MM-DD) actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_horas_registro():
    id_registro = solicitar_id_de("registro de tiempo")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if registro is None:
            print("No existe registro de tiempo con ese ID.")
            return
        nuevo = solicitar("Horas", validar_horas)
        if nuevo == registro.obtenerHorasTrabajadas():
            print("El valor es el mismo; no hay cambios.")
            return
        registro.cambiarHorasTrabajadas(nuevo)
        filas = RegistroTiempoDAO.actualizar(registro)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Horas actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def actualizar_tarea_registro():
    id_registro = solicitar_id_de("registro de tiempo")
    IntegrityError, OperationalError = tipos_errores_bd()
    try:
        registro = RegistroTiempoDAO.buscar_por_id(id_registro)
        if registro is None:
            print("No existe registro de tiempo con ese ID.")
            return
        nuevo = solicitar("Tarea", validar_texto_obligatorio)
        if nuevo == registro.obtenerDescripcionTarea():
            print("El valor es el mismo; no hay cambios.")
            return
        registro.cambiarDescripcionTarea(nuevo)
        filas = RegistroTiempoDAO.actualizar(registro)
    except IntegrityError:
        print("No se pudo actualizar: revisa las restricciones de la BD.")
    except OperationalError:
        print("No se pudo completar la actualización.")
    else:
        if filas == 1:
            print("Tarea actualizado correctamente.")
        else:
            print("No hubo cambios en la BD; consulta el ID otra vez.")


def eliminar_registro():
    eliminar_con_confirmacion("registro de tiempo", RegistroTiempoDAO.buscar_por_id,
                              RegistroTiempoDAO.eliminar)


def menu_registros_tiempo():
    while True:
        print("\n--- ECOTECH: REGISTROS DE TIEMPO ---")
        print("1. Registrar\n2. Listar\n3. Buscar por ID")
        print("4. Actualizar fecha\n5. Actualizar horas\n6. Actualizar tarea")
        print("7. Eliminar\n0. Volver")
        opcion = input("Opción: ").strip()
        if opcion == "1":
            crear_registro()
        elif opcion == "2":
            listar_registros()
        elif opcion == "3":
            buscar_registro()
        elif opcion == "4":
            actualizar_fecha_registro()
        elif opcion == "5":
            actualizar_horas_registro()
        elif opcion == "6":
            actualizar_tarea_registro()
        elif opcion == "7":
            eliminar_registro()
        elif opcion == "0":
            break
        else:
            print("Elige una opción entre 0 y 7.")
