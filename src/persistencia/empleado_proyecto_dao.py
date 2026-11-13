from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoProyectoDAO:
    # La tabla puente representa la relación muchos a muchos (N:M) del UML.
    @staticmethod
    def asignar(empleado, proyecto):
        if empleado.id is None or proyecto.id is None:
            raise ValueError("Primero debes guardar el empleado y el proyecto.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            valores = (empleado.id, proyecto.id)
            consulta = ("SELECT empleado_id FROM empleado_proyecto "
                        f"WHERE empleado_id = {marcador} AND proyecto_id = {marcador}")
            cursor.execute(consulta, valores)
            if cursor.fetchone() is not None:
                return False  # La pareja ya existe, no la repetimos.

            sql = ("INSERT INTO empleado_proyecto (empleado_id, proyecto_id) "
                   f"VALUES ({marcador}, {marcador})")
            cursor.execute(sql, valores)
            conexion.commit()
            return True
        finally:
            conexion.close()

    @staticmethod
    def listar_por_empleado(empleado_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"SELECT proyecto_id FROM empleado_proyecto WHERE empleado_id = {marcador} ORDER BY proyecto_id",
                (empleado_id,)
            )
            filas = cursor.fetchall()
            return [fila[0] for fila in filas]
        finally:
            conexion.close()

    @staticmethod
    def listar_por_proyecto(proyecto_id):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"SELECT empleado_id FROM empleado_proyecto WHERE proyecto_id = {marcador} ORDER BY empleado_id",
                (proyecto_id,)
            )
            filas = cursor.fetchall()
            return [fila[0] for fila in filas]
        finally:
            conexion.close()
