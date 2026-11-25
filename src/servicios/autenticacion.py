
import bcrypt

from dominio.usuario import Usuario
from persistencia.empleado_dao import EmpleadoDAO
from persistencia.usuario_dao import UsuarioDAO

MAX_BYTES_BCRYPT = 72
USUARIO_RESERVADO = "admin"


def crear_hash(clave):
    clave = Usuario.validar_clave(clave)
    clave_bytes = clave.encode("utf-8")

    if len(clave_bytes) > MAX_BYTES_BCRYPT:
        raise ValueError("Máximo 72 bytes UTF-8 para bcrypt.")

    return bcrypt.hashpw(
        clave_bytes, bcrypt.gensalt()
    ).decode("utf-8")



def crear_cuenta(empleado_id, nombre, clave, rol="empleado"):
    if type(empleado_id) is not int or empleado_id <= 0:
        raise ValueError("El ID del empleado debe ser positivo.")

    nombre = Usuario.normalizar_usuario(nombre)
    password_hash = crear_hash(clave)

    if EmpleadoDAO.buscar_por_id(empleado_id) is None:
        raise ValueError("No existe un empleado con ese ID.")

    usuario = Usuario(nombre, password_hash, empleado_id, rol=rol)
    return UsuarioDAO.insertar(usuario)


def registrar_usuario(empleado_id, nombre, clave):
    nombre = Usuario.normalizar_usuario(nombre)

    if nombre == USUARIO_RESERVADO:
        raise ValueError("Ese nombre de usuario está reservado.")

    return crear_cuenta(empleado_id, nombre, clave)


def verificar_clave_actual(id_usuario, clave_actual):
    if not isinstance(clave_actual, str):
        return None

    datos = clave_actual.encode("utf-8")

    if not 0 < len(datos) <= MAX_BYTES_BCRYPT:
        return None

    cuenta = UsuarioDAO.buscar_por_id(id_usuario)

    if cuenta is None:
        return None

    if not bcrypt.checkpw(datos, cuenta.password_hash.encode("utf-8")):
        return None

    return cuenta


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

    if not bcrypt.checkpw(
        datos, cuenta.password_hash.encode("utf-8")
    ):
        return None

    return cuenta


def buscar_usuario_por_nombre(nombre):
    nombre = Usuario.normalizar_usuario(nombre)
    return UsuarioDAO.buscar_por_nombre(nombre)


def buscar_usuario_por_id(id_usuario):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise ValueError("El ID debe ser un número entero positivo.")

    return UsuarioDAO.buscar_por_id(id_usuario)


def listar_usuarios():
    return UsuarioDAO.listar()


def actualizar_usuario(id_usuario, nuevo_nombre=None, nueva_clave=None):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise ValueError("El ID debe ser un número entero positivo.")

    cuenta = UsuarioDAO.buscar_por_id(id_usuario)

    if cuenta is None:
        return 0

    if nuevo_nombre is not None:
        nuevo_nombre = Usuario.normalizar_usuario(nuevo_nombre)

        if cuenta.nombre_usuario == USUARIO_RESERVADO and nuevo_nombre != USUARIO_RESERVADO:
            raise ValueError("La cuenta admin no puede cambiar su nombre de usuario.")

        if nuevo_nombre == USUARIO_RESERVADO and cuenta.nombre_usuario != USUARIO_RESERVADO:
            raise ValueError("Ese nombre de usuario está reservado.")

        cuenta.nombre_usuario = nuevo_nombre

    if nueva_clave is not None:
        cuenta.password_hash = crear_hash(nueva_clave)

    return UsuarioDAO.actualizar(cuenta)


def cambiar_clave(id_usuario, nueva_clave):
    return actualizar_usuario(
        id_usuario,
        nueva_clave=nueva_clave
    )


def eliminar_usuario(id_usuario):
    if type(id_usuario) is not int or id_usuario <= 0:
        raise ValueError("El ID debe ser un número entero positivo.")

    cuenta = UsuarioDAO.buscar_por_id(id_usuario)

    if cuenta is None:
        return 0

    return UsuarioDAO.eliminar(id_usuario)


def cambiar_nombre_propio(id_usuario, clave_actual, nuevo_nombre):
    cuenta = verificar_clave_actual(id_usuario, clave_actual)

    if cuenta is None:
        raise ValueError("La contraseña actual no es correcta.")

    return actualizar_usuario(id_usuario, nuevo_nombre=nuevo_nombre)


def cambiar_clave_propia(id_usuario, clave_actual, nueva_clave):
    cuenta = verificar_clave_actual(id_usuario, clave_actual)

    if cuenta is None:
        raise ValueError("La contraseña actual no es correcta.")

    nuevo_hash = crear_hash(nueva_clave)

    if bcrypt.checkpw(nueva_clave.encode("utf-8"), cuenta.password_hash.encode("utf-8")):
        raise ValueError("La nueva contraseña debe ser distinta a la actual.")

    cuenta.password_hash = nuevo_hash
    return UsuarioDAO.actualizar(cuenta)


def eliminar_cuenta_propia(id_usuario, clave_actual):
    cuenta = verificar_clave_actual(id_usuario, clave_actual)

    if cuenta is None:
        raise ValueError("La contraseña actual no es correcta.")

    if cuenta.nombre_usuario == USUARIO_RESERVADO:
        raise ValueError("La cuenta admin no se puede eliminar desde aquí.")

    return UsuarioDAO.eliminar(id_usuario)
