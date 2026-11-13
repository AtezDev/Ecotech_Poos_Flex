from persistencia.conexion import abrir_conexion, obtener_motor


class DepartamentoDAO:
    @staticmethod
    def insertar(departamento):
        if departamento.id is not None:
            raise ValueError("Este departamento ya fue guardado.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"INSERT INTO departamento (nombre, gerente) VALUES ({marcador}, {marcador})"
            # Los valores van separados del SQL, nunca concatenados con el usuario.
            cursor.execute(sql, (departamento.nombre, departamento.gerente))
            nuevo_id = cursor.lastrowid
            conexion.commit()
            departamento.id = nuevo_id
            return departamento
        finally:
            conexion.close()
