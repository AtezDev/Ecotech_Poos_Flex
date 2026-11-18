from datetime import date
from dominio.departamento import Departamento
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoDAO:
    @staticmethod
    def insertar(empleado, departamento=None):
        if empleado.id is not None:
            raise ValueError("Este empleado ya tiene un ID de base de datos.")
        if departamento is not None and departamento.id is None:
            raise ValueError("Primero debes guardar el departamento.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            departamento_id = departamento.id if departamento is not None else None
            sql = f"""INSERT INTO empleado
                (nombre, direccion, telefono, correo, fecha_inicio_contrato,
                 salario, departamento_id)
                VALUES ({marcador}, {marcador}, {marcador}, {marcador},
                        {marcador}, {marcador}, {marcador})"""
            valores = (empleado.nombre, empleado.direccion, empleado.telefono,
                       empleado.correoElectronico, empleado.fechaInicioContrato.isoformat(),
                       empleado.salario, departamento_id)
            cursor.execute(sql, valores)
            nuevo_id = cursor.lastrowid  # El ID lo asignó la BD.
            conexion.commit()           # Confirmamos el INSERT.
            empleado.id = nuevo_id
            return empleado
        finally:
            conexion.close()            # Cierre incluso cuando hay error.

    @staticmethod
    def reconstruir(fila):
        (id_empleado, nombre, direccion, telefono, correo, fecha, salario,
         id_departamento, nombre_departamento, gerente) = fila
        empleado = Empleado(nombre, direccion, telefono, correo,
                            date.fromisoformat(str(fecha)), float(salario), id=id_empleado)
        if id_departamento is not None:
            departamento = Departamento(nombre_departamento, gerente, id=id_departamento)
            departamento.agregar_empleado(empleado)
        return empleado

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            cursor.execute("""SELECT e.id, e.nombre, e.direccion, e.telefono, e.correo,
                           e.fecha_inicio_contrato, e.salario, d.id, d.nombre, d.gerente
                           FROM empleado e LEFT JOIN departamento d
                           ON e.departamento_id = d.id ORDER BY e.id""")
            filas = cursor.fetchall()
        finally:
            conexion.close()

        empleados = []
        for fila in filas:
            empleados.append(EmpleadoDAO.reconstruir(fila))
        return empleados

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""SELECT e.id, e.nombre, e.direccion, e.telefono, e.correo,
                      e.fecha_inicio_contrato, e.salario, d.id, d.nombre, d.gerente
                      FROM empleado e LEFT JOIN departamento d
                      ON e.departamento_id = d.id WHERE e.id = {marcador}"""
            cursor.execute(sql, (id_empleado,))
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        return EmpleadoDAO.reconstruir(fila)

    @staticmethod
    def actualizar_departamento(empleado):
        if empleado.id is None:
            raise ValueError("Primero debes guardar el empleado.")
        if empleado.departamento is not None and empleado.departamento.id is None:
            raise ValueError("Primero debes guardar el departamento.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            departamento_id = empleado.departamento.id if empleado.departamento is not None else None
            sql = f"UPDATE empleado SET departamento_id = {marcador} WHERE id = {marcador}"
            cursor.execute(sql, (departamento_id, empleado.id))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()

    @staticmethod
    def actualizar(empleado):
        if empleado.id is None:
            raise ValueError("Primero debes guardar el empleado.")
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = (f"UPDATE empleado SET nombre = {marcador}, direccion = {marcador}, "
                   f"telefono = {marcador}, correo = {marcador}, salario = {marcador} "
                   f"WHERE id = {marcador}")
            valores = (empleado.nombre, empleado.direccion, empleado.telefono,
                       empleado.correoElectronico, empleado.salario, empleado.id)
            cursor.execute(sql, valores)
            filas = cursor.rowcount
            conexion.commit()
            return filas  # 1: actualizado; 0: no había registro con ese ID.
        finally:
            conexion.close()

    @staticmethod
    def eliminar(id_empleado):
        # Sin ON DELETE CASCADE: si hay relaciones, la BD debe impedir borrar.
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"DELETE FROM empleado WHERE id = {marcador}"
            cursor.execute(sql, (id_empleado,))
            filas = cursor.rowcount
            conexion.commit()
            return filas
        finally:
            conexion.close()
