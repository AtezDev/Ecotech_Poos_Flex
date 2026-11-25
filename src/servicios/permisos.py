from dominio.usuario import Usuario


def exigir_sesion(usuario):
    if usuario is None:
        raise PermissionError("Inicie sesión.")

    if not isinstance(usuario, Usuario):
        raise PermissionError("Sesión inválida.")

    if usuario.rol not in Usuario.ROLES:
        raise PermissionError("Acceso no permitido.")


def exigir_admin(usuario):
    exigir_sesion(usuario)

    if usuario.rol != "admin":
        raise PermissionError("Acción solo para administrador.")
