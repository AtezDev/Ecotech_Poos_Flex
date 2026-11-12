from persistencia.conexion import abrir_conexion, obtener_motor


class ProyectoDAO:
    @staticmethod
    def insertar(proyecto):
        if proyecto.id is not None:
            raise ValueError("Este objeto ya tiene un ID de base de datos.")
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        sql = (f"INSERT INTO proyecto (nombre, descripcion, fecha_inicio) "
               f"VALUES ({marcador}, {marcador}, {marcador})")
        valores = (proyecto.nombre, proyecto.descripcion,
                   proyecto.fechaInicio.isoformat())
        cursor.execute(sql, valores)
        nuevo_id = cursor.lastrowid
        conexion.commit()
        proyecto.id = nuevo_id
        conexion.close()
        return proyecto
