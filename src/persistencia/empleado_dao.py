from datetime import date
from dominio.empleado import Empleado
from persistencia.conexion import abrir_conexion, obtener_motor


class EmpleadoDAO:
    @staticmethod
    def insertar(empleado, departamento=None):
        if empleado.id is not None:
            raise ValueError("Este objeto ya tiene un ID de base de datos.")
        conexion = abrir_conexion()
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
        nuevo_id = cursor.lastrowid
        conexion.commit()
        empleado.id = nuevo_id
        conexion.close()
        return empleado

    @staticmethod
    def listar():
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        cursor.execute("""SELECT id, nombre, direccion, telefono, correo,
                       fecha_inicio_contrato, salario FROM empleado ORDER BY id""")
        filas = cursor.fetchall()
        conexion.close()

        empleados = []
        for id_empleado, nombre, direccion, telefono, correo, fecha, salario in filas:
            empleado = Empleado(
                nombre=nombre,
                direccion=direccion,
                telefono=telefono,
                correoElectronico=correo,
                fechaInicioContrato=date.fromisoformat(str(fecha)),
                salario=float(salario),
                id=id_empleado
            )
            empleados.append(empleado)
        return empleados

    @staticmethod
    def buscar_por_id(id_empleado):
        conexion = abrir_conexion()
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"
        sql = f"""SELECT id, nombre, direccion, telefono, correo,
                  fecha_inicio_contrato, salario FROM empleado
                  WHERE id = {marcador}"""
        cursor.execute(sql, (id_empleado,))
        fila = cursor.fetchone()
        conexion.close()

        if fila is None:
            return None

        id_encontrado, nombre, direccion, telefono, correo, fecha, salario = fila
        return Empleado(
            nombre=nombre,
            direccion=direccion,
            telefono=telefono,
            correoElectronico=correo,
            fechaInicioContrato=date.fromisoformat(str(fecha)),
            salario=float(salario),
            id=id_encontrado
        )
