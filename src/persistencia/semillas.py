
from datetime import date

from dominio.departamento import Departamento
from dominio.empleado import Empleado

from persistencia.conexion import abrir_conexion, obtener_motor
from persistencia.departamento_dao import DepartamentoDAO
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO

from servicios.autenticacion import registrar_usuario


DEPARTAMENTOS = [
    ("Soporte", "ana.torres@ecotech.cl"),
    ("Desarrollo", "maria.perez@ecotech.cl"),
]

EMPLEADOS = [
    ("Ana Torres", "Av. del Mar 100, La Serena", "+56911110001",
     "ana.torres@ecotech.cl", date(2026, 3, 2), 950000, "Soporte"),

    ("Luis Soto", "Calle Prat 250, La Serena", "+56911110002",
     "luis.soto@ecotech.cl", date(2026, 4, 6), 880000, "Soporte"),

    ("María Pérez", "Los Carrera 45, Coquimbo", "+56911110003",
     "maria.perez@ecotech.cl", date(2026, 5, 4), 1100000, "Desarrollo"),
]

USUARIO_ADMIN = "admin"
CLAVE_ADMIN_INICIAL = "EcoTech2026!Admin"


def buscar_id_departamento(nombre):
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        cursor.execute(
            f"SELECT id FROM departamento WHERE nombre = {marcador}",
            (nombre,)
        )
        fila = cursor.fetchone()
    finally:
        conexion.close()

    if fila is None:
        return None

    return fila[0]


def buscar_id_empleado(correo):
    conexion = abrir_conexion()
    try:
        cursor = conexion.cursor()
        marcador = "?" if obtener_motor() == "sqlite" else "%s"

        cursor.execute(
            f"SELECT id FROM empleado WHERE correo = {marcador}",
            (correo,)
        )
        fila = cursor.fetchone()
    finally:
        conexion.close()

    if fila is None:
        return None

    return fila[0]


def asegurar_admin_inicial():
    # No modificar una cuenta admin que ya exista.
    if UsuarioDAO.buscar_por_nombre(USUARIO_ADMIN) is not None:
        return False

    empleados = EmpleadoDAO.listar()

    for empleado in empleados:
        cuenta = UsuarioDAO.buscar_por_empleado_id(empleado.id)

        if cuenta is None:
            registrar_usuario(
                empleado.id,
                USUARIO_ADMIN,
                CLAVE_ADMIN_INICIAL
            )
            return True

    return False


def cargar_semillas():
    empleados_nuevos = []
    departamentos_nuevos = 0

    for nombre, direccion, telefono, correo, fecha, salario, nombre_dep in EMPLEADOS:
        if buscar_id_empleado(correo) is None:
            empleado = Empleado(
                nombre, direccion, telefono, correo, fecha, salario
            )
            EmpleadoDAO.insertar(empleado)
            empleados_nuevos.append((empleado, nombre_dep))

    for nombre, correo_gerente in DEPARTAMENTOS:
        if buscar_id_departamento(nombre) is None:
            gerente = None
            id_gerente = buscar_id_empleado(correo_gerente)

            if id_gerente is not None:
                gerente = EmpleadoDAO.buscar_por_id(id_gerente)

            DepartamentoDAO.insertar(
                Departamento(nombre, gerente)
            )
            departamentos_nuevos += 1

    for empleado, nombre_dep in empleados_nuevos:
        id_departamento = buscar_id_departamento(nombre_dep)
        departamento = DepartamentoDAO.buscar_por_id(id_departamento)

        if departamento is not None:
            departamento.agregar_empleado(empleado)
            EmpleadoDAO.actualizar_departamento(empleado)


    return departamentos_nuevos, len(empleados_nuevos)
