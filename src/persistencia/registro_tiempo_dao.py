from persistencia.conexion import abrir_conexion, obtener_motor


class RegistroTiempoDAO:
    @staticmethod
    def insertar(registro):
        if registro.empleado is None or registro.proyecto is None:
            raise ValueError("El registro necesita un empleado y un proyecto.")
        if registro.empleado.id is None or registro.proyecto.id is None:
            raise ValueError("Primero debes guardar el empleado y el proyecto.")

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        consulta = ("SELECT empleado_id FROM empleado_proyecto "
                    f"WHERE empleado_id = {marcador} AND proyecto_id = {marcador}")
        cursor.execute(consulta, (registro.empleado.id, registro.proyecto.id))
        if cursor.fetchone() is None:
            conexion.close()
            raise ValueError("El empleado no está asignado al proyecto.")

        sql = ("INSERT INTO registro_tiempo "
               "(fecha, horas_trabajadas, descripcion_tarea, empleado_id, proyecto_id) "
               f"VALUES ({marcador}, {marcador}, {marcador}, {marcador}, {marcador})")
        valores = (registro.fecha.isoformat(), registro.horasTrabajadas,
                   registro.descripcionTarea, registro.empleado.id,
                   registro.proyecto.id)
        cursor.execute(sql, valores)
        registro.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return registro
