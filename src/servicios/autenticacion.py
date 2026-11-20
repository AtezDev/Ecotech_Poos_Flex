import bcrypt
from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")
    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")


def registrar_usuario(empleado_id, nombre, clave):
    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("El ID del empleado debe ser positivo.")
    nombre = Usuario.normalizar_usuario(nombre)
    password_hash = crear_hash(clave)
    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")
    usuario = Usuario(nombre, password_hash, empleado_id)
    return UsuarioDAO.insertar(usuario)


def autenticar(nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)
    if not isinstance(clave, str):
        return None
    datos = clave.encode("utf-8")
    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None
    cuenta = UsuarioDAO.buscar_por_nombre(nombre)

    if cuenta is None:
        return None
    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None
    return cuenta
