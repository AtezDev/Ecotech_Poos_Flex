from persistencia.conexion import abrir_conexion, obtener_motor


class DepartamentoDAO:
    @staticmethod
    def insertar(departamento):
        if departamento.id is not None:
            raise ValueError("Este objeto ya tiene un ID de base de datos.")
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        sql = f"INSERT INTO departamento (nombre, gerente) VALUES ({marcador}, {marcador})"
        cursor.execute(sql, (departamento.nombre, departamento.gerente))
        nuevo_id = cursor.lastrowid
        conexion.commit()
        departamento.id = nuevo_id
        conexion.close()
        return departamento
