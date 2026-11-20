from dominio.usuario import Usuario
from persistencia.conexion import abrir_conexion, obtener_motor


class UsuarioDAO:
    @staticmethod
    def insertar(usuario):
        if usuario.id is not None:
            raise ValueError("Esta cuenta ya fue guardada.")

        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""INSERT INTO usuario (nombre_usuario, password_hash, empleado_id)
                      VALUES ({marcador}, {marcador}, {marcador})"""
            cursor.execute(sql, (usuario.nombre_usuario, usuario.password_hash,
                                 usuario.empleado_id))
            nuevo_id = cursor.lastrowid
            conexion.commit()
            usuario.id = nuevo_id
            return usuario
        finally:
            conexion.close()

    @staticmethod
    def buscar_por_nombre(nombre_usuario):
        conexion = abrir_conexion()
        try:
            cursor = conexion.cursor()
            marcador = "?" if obtener_motor() == "sqlite" else "%s"
            sql = f"""SELECT id, nombre_usuario, password_hash, empleado_id
                      FROM usuario WHERE nombre_usuario = {marcador}"""
            cursor.execute(sql, (nombre_usuario,))
            fila = cursor.fetchone()
        finally:
            conexion.close()
        if fila is None:
            return None
        id_cuenta, nombre, password_hash, empleado_id = fila
        return Usuario(nombre, password_hash, empleado_id, id=id_cuenta)
