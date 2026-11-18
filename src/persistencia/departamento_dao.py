from datetime import date
from dominio.departamento import Departamento
from dominio.empleado import Empleado
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

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("SELECT id, nombre, gerente FROM departamento ORDER BY id")
            filas = cursor.fetchall()
        finally:
            conexion.close()
        departamentos = []
        for id_departamento, nombre, gerente in filas:
            departamentos.append(Departamento(nombre, gerente, id=id_departamento))
        return departamentos

    @staticmethod
    def buscar_por_id(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"SELECT id, nombre, gerente FROM departamento WHERE id = {marcador}",
                           (id_departamento,))
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return Departamento(fila[1], fila[2], id=fila[0])

    @staticmethod
    def actualizar(departamento):
        if departamento.id is None:
            raise ValueError("Primero debes guardar el departamento.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"UPDATE departamento SET nombre = {marcador}, gerente = {marcador} WHERE id = {marcador}"
            cursor.execute(sql, (departamento.nombre, departamento.gerente, departamento.id))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(f"DELETE FROM departamento WHERE id = {marcador}", (id_departamento,))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def asignar_empleado(id_empleado, id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"UPDATE empleado SET departamento_id = {marcador} WHERE id = {marcador}"
            cursor.execute(sql, (id_departamento, id_empleado))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def quitar_empleado(id_empleado):
        return DepartamentoDAO.asignar_empleado(id_empleado, None)

    @staticmethod
    def listar_empleados(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            cursor.execute(
                f"SELECT id FROM empleado WHERE departamento_id = {marcador} ORDER BY id",
                (id_departamento,)
            )
            filas = cursor.fetchall()
            ids = []
            for fila in filas:
                ids.append(fila[0])
            return ids
        finally:
            conexion.close()

    @staticmethod
    def reconstruir_departamento(filas):
        if not filas:
            return None
        departamento = Departamento(filas[0][1], filas[0][2], id=filas[0][0])
        for _, _, _, id_emp, nombre, direccion, telefono, correo, fecha, salario in filas:
            if id_emp is not None:
                empleado = Empleado(nombre, direccion, telefono, correo,
                                    date.fromisoformat(str(fecha)), float(salario), id=id_emp)
                departamento.agregar_empleado(empleado)
        return departamento

    @staticmethod
    def buscar_con_empleados(id_departamento):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""SELECT d.id, d.nombre, d.gerente, e.id, e.nombre, e.direccion,
                      e.telefono, e.correo, e.fecha_inicio_contrato, e.salario
                      FROM departamento d LEFT JOIN empleado e
                      ON e.departamento_id = d.id
                      WHERE d.id = {marcador} ORDER BY e.id"""
            cursor.execute(sql, (id_departamento,))
            filas = cursor.fetchall()
        finally:
            conexion.close()
        return DepartamentoDAO.reconstruir_departamento(filas)
