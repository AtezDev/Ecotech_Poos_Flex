from datetime import date
from dominio.registro_tiempo import RegistroTiempo
from persistencia.conexion import abrir_conexion, obtener_motor
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.proyecto_dao import ProyectoDAO


class RegistroTiempoDAO:
    @staticmethod
    def insertar(registro):
        if registro.empleado is None or registro.proyecto is None:
            raise ValueError("El registro necesita un empleado y un proyecto.")
        if registro.empleado.id is None or registro.proyecto.id is None:
            raise ValueError("Primero debes guardar el empleado y el proyecto.")
        if registro.id is not None:
            raise ValueError("Este registro ya fue guardado.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            consulta = ("SELECT empleado_id FROM empleado_proyecto "
                        f"WHERE empleado_id = {marcador} AND proyecto_id = {marcador}")
            cursor.execute(consulta, (registro.empleado.id, registro.proyecto.id))
            if cursor.fetchone() is None:
                raise ValueError("El empleado no está asignado al proyecto.")

            sql = ("INSERT INTO registro_tiempo "
                   "(fecha, horas_trabajadas, descripcion_tarea, empleado_id, proyecto_id) "
                   f"VALUES ({marcador}, {marcador}, {marcador}, {marcador}, {marcador})")
            valores = (registro.fecha.isoformat(), registro.horasTrabajadas,
                       registro.descripcionTarea, registro.empleado.id,
                       registro.proyecto.id)
            cursor.execute(sql, valores)
            nuevo_id = cursor.lastrowid
            conexion.commit()
            registro.id = nuevo_id
            return registro
        finally:
            conexion.close()

    @staticmethod
    def reconstruir(fila):
        id_registro, fecha, horas, tarea, id_empleado, id_proyecto = fila
        registro = RegistroTiempo(date.fromisoformat(str(fecha)), float(horas), tarea, id=id_registro)
        registro.empleado = EmpleadoDAO.buscar_por_id(id_empleado)
        registro.proyecto = ProyectoDAO.buscar_por_id(id_proyecto)
        return registro

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT id, fecha, horas_trabajadas, descripcion_tarea,
                           empleado_id, proyecto_id FROM registro_tiempo ORDER BY id""")
            filas = cursor.fetchall()
        finally:
            conexion.close()
        registros = []
        for fila in filas:
            registros.append(RegistroTiempoDAO.reconstruir(fila))
        return registros

    @staticmethod
    def buscar_por_id(id_registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""SELECT id, fecha, horas_trabajadas, descripcion_tarea,
                      empleado_id, proyecto_id FROM registro_tiempo WHERE id = {marcador}"""
            cursor.execute(sql, (id_registro,))
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return RegistroTiempoDAO.reconstruir(fila)

    @staticmethod
    def actualizar(registro):
        if registro.id is None:
            raise ValueError("Primero debes guardar el registro.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = (f"UPDATE registro_tiempo SET fecha = {marcador}, horas_trabajadas = {marcador}, "
                   f"descripcion_tarea = {marcador} WHERE id = {marcador}")
            valores = (registro.fecha.isoformat(), registro.horasTrabajadas,
                       registro.descripcionTarea, registro.id)
            cursor.execute(sql, valores)
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_registro):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"DELETE FROM registro_tiempo WHERE id = {marcador}", (id_registro,))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()
