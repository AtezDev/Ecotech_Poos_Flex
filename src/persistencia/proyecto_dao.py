from persistencia.conexion import abrir_conexion, obtener_motor


class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        sql = (f"INSERT INTO proyecto (nombre, descripcion, fecha_inicio) "
               f"VALUES ({marcador}, {marcador}, {marcador})")
        valores = (proyecto.nombre, proyecto.descripcion,
                   proyecto.fechaInicio.isoformat())
        cursor.execute(sql, valores)
        proyecto.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return proyecto
