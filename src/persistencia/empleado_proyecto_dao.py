from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoProyectoDAO:
    @staticmethod
    def asignar(empleado, proyecto):
        if empleado.id is None or proyecto.id is None:
            raise ValueError("Primero debes guardar el empleado y el proyecto.")

        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        consulta = ("SELECT empleado_id FROM empleado_proyecto "
                    f"WHERE empleado_id = {marcador} AND proyecto_id = {marcador}")
        valores = (empleado.id, proyecto.id)
        cursor.execute(consulta, valores)
        if cursor.fetchone() is not None:
            conexion.close()
            return False

        sql = ("INSERT INTO empleado_proyecto (empleado_id, proyecto_id) "
               f"VALUES ({marcador}, {marcador})")
        cursor.execute(sql, valores)
        conexion.commit()
        conexion.close()
        return True
