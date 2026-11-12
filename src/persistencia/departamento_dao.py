from persistencia.conexion import abrir_conexion, obtener_motor


class DepartamentoDAO:
    @staticmethod
    def insertar(departamento):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        sql = f"INSERT INTO departamento (nombre, gerente) VALUES ({marcador}, {marcador})"
        cursor.execute(sql, (departamento.nombre, departamento.gerente))
        departamento.id = cursor.lastrowid
        conexion.commit()
        conexion.close()
        return departamento
